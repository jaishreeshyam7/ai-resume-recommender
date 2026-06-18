import json
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

JD_TEXT = """
Senior AI Engineer
retrieval
ranking
recommendation systems
candidate matching
embeddings
vector databases
evaluation frameworks
NDCG
MRR
Python
learning to rank
semantic search
hybrid retrieval
vector search
"""

KEYWORDS = [
    "retrieval",
    "ranking",
    "recommendation",
    "search",
    "embedding",
    "vector",
    "semantic search",
    "information retrieval",
    "rerank",
    "matching",
    "vector database",
    "rag",
    "llm",
    "machine learning",
    "learning to rank",
    "ndcg",
    "mrr"
]

AI_TITLES = [
    "ml engineer",
    "machine learning engineer",
    "ai engineer",
    "data scientist",
    "nlp engineer",
    "search engineer",
    "backend engineer",
    "software engineer",
    "data engineer",
    "applied scientist",
    "recommendation systems engineer",
    "ai research engineer"
]

NEGATIVE_TITLES = [
    "marketing",
    "accountant",
    "civil engineer",
    "mechanical engineer",
    "customer support",
    "operations manager",
    "hr",
    "content writer"
]

CONSULTING = {
    "tcs",
    "infosys",
    "wipro",
    "accenture",
    "cognizant",
    "capgemini"
}

def passes_hard_filter(candidate):
    profile = candidate["profile"]
    exp = profile["years_of_experience"]

    if exp < 4:
        return False

    skills = [
        s["name"].lower()
        for s in candidate["skills"] 
    ]
    
    if "python" not in skills:
        return False

    total_exp_months = exp * 12

    for skill in candidate["skills"]:
        duration = skill.get("duration_months", 0)
        if duration > total_exp_months:
            return False

    text = profile.get("summary", "").lower()

    for job in candidate.get("career_history", []):
        text += " " + job.get("description", "").lower()

    retrieval_evidence = any(
        kw in text
        for kw in KEYWORDS
    )

    return retrieval_evidence


def score_candidate(candidate):
    score = 0
    profile = candidate["profile"]
    exp = profile["years_of_experience"]
    title = profile["current_title"].lower()

    if 5 <= exp <= 9:
        score += 20
    elif exp >= 4:
        score += 10

    for t in AI_TITLES:
        if t in title:
            score += 20
            break

    for t in NEGATIVE_TITLES:
        if t in title:
            score -= 20
            break

    skills = [
        s["name"].lower()
        for s in candidate["skills"]
    ]

    important_skills = [
        "python",
        "milvus",
        "pinecone",
        "qdrant",
        "faiss",
        "nlp",
        "lora",
        "embedding",
        "elasticsearch",
        "opensearch",
        "weaviate"
    ]

    for skill in important_skills:
        if skill in skills:
            score += 5

    text = profile.get("summary", "").lower()

    for job in candidate.get("career_history", []):
        text += " " + job.get("description", "").lower()

    for kw in KEYWORDS:
        if kw in text:
            score += 10

    candidate_text = (
        profile.get("headline", "") + " " +
        profile.get("summary", "") + " " +
        text
    )

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform(
            [JD_TEXT, candidate_text]
        )
        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]
        score += similarity * 100
    except:
        pass

    companies = [
        job["company"].lower()
        for job in candidate.get("career_history", [])
    ]

    if len(companies) > 0 and all(
        c in CONSULTING
        for c in companies
    ):
        score -= 30

    signals = candidate.get("redrob_signals", {})

    score += signals.get("recruiter_response_rate", 0) * 20
    score += signals.get("interview_completion_rate", 0) * 15
    score += max(signals.get("github_activity_score", 0), 0) * 0.2

    if signals.get("open_to_work_flag", False):
        score += 10

    return round(score, 4)


print("Running ranker...")

results = []
total = 0
passed = 0

with open("candidates.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        total += 1
        candidate = json.loads(line)

        if not passes_hard_filter(candidate):
            continue

        passed += 1
        score = score_candidate(candidate)

        # Added .get() to prevent KeyError if missing
        response_rate = candidate.get("redrob_signals", {}).get("recruiter_response_rate", 0)

        reasoning = (
            f"{candidate['profile']['years_of_experience']:.1f} yrs experience; "
            f"{candidate['profile']['current_title']}; "
            f"response rate {response_rate:.2f}"
        )

        results.append({
            "candidate_id": candidate["candidate_id"],
            "title": candidate["profile"]["current_title"],
            "score": score,
            "reasoning": reasoning
        })

results.sort(
    key=lambda x: x["score"],
    reverse=True
)

print("Total:", total)
print("Passed:", passed)

top100 = results[:100]

with open("submission.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    writer.writerow([
        "candidate_id",
        "rank",
        "score",
        "reasoning"
    ])

    for rank, row in enumerate(top100, start=1):
        writer.writerow([
            row["candidate_id"],
            rank,
            row["score"],
            row["reasoning"]
        ])

print("submission.csv generated successfully")