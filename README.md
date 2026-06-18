# Intelligent Candidate Discovery & Ranking System

## Overview

This project was developed for the **Redrob AI Intelligent Candidate Discovery & Ranking Challenge**.

The objective is to identify the **Top 100 most relevant candidates** for a Senior AI Engineer role from a dataset of **100,000 candidate profiles** while satisfying the challenge constraints:

- CPU-only execution
- Runtime under 5 minutes
- Explainable ranking
- No external APIs or LLM inference

---

# Solution Overview

Our solution follows a lightweight three-stage ranking pipeline.

```
Job Description
        │
        ▼
Requirement Extraction
        │
        ▼
Candidate Dataset (100K)
        │
        ▼
Hard Filtering
        │
        ▼
Semantic Matching
        │
        ▼
Behavioral Signal Scoring
        │
        ▼
Final Ranking
        │
        ▼
Top 100 Candidates
```

---

# Approach

## 1. Hard Filtering

Candidates are first filtered using mandatory requirements extracted from the Job Description.

Filters include:

- Minimum experience
- Python proficiency
- Retrieval/Search evidence
- Suspicious skill duration detection
- Basic profile consistency checks

This reduces the search space dramatically before expensive scoring begins.

---

## 2. Semantic Matching

Instead of relying on simple keyword matching, the system measures semantic relevance between the Job Description and candidate profiles.

Candidate information used:

- Summary
- Skills
- Career history

Technique:

- TF-IDF Vectorization
- Cosine Similarity

This helps identify candidates with relevant experience even if exact keywords differ.

---

## 3. Multi-Signal Scoring

Each candidate receives a composite score using multiple signals.

Technical Signals

- AI/ML role titles
- Python
- Retrieval systems
- Ranking systems
- Recommendation systems
- Vector databases
- Embedding models
- NLP experience

Behavioral Signals

- Recruiter response rate
- GitHub activity
- Interview completion rate
- Open-to-work status

Career Signals

- Product company experience
- Consulting-only penalty
- Career history relevance

---

# Ranking Formula

The final score combines multiple components:

```
Final Score =
Technical Score
+ Semantic Similarity
+ Behavioral Signals
+ Career Context
− Penalties
```

Candidates are sorted in descending order and the Top 100 are selected.

---

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core implementation |
| Scikit-learn | TF-IDF & Cosine Similarity |
| JSON | Candidate dataset parsing |
| CSV | Submission generation |
| Rule-based Heuristics | Candidate filtering |
| Redrob Behavioral Signals | Final score enhancement |

---

# Project Structure

```
.
├── candidates.jsonl
├── candidate_schema.json
├── job_description.docx
├── rank.py
├── validate_submission.py
├── submission.csv
├── submission_metadata.yaml
└── README.md
```

---

# Running the Solution

Install dependencies

```bash
pip install scikit-learn
```

Run

```bash
python rank.py
```

The script generates

```
submission.csv
```

---

# Validation

Validate the generated submission using

```bash
python validate_submission.py submission.csv
```

Expected Output

```
Submission is valid.
```

---

# Performance

Dataset Size

- 100,000 candidates

Candidates after filtering

- ~850

Final Output

- Top 100 ranked candidates

Execution

- CPU only
- Lightweight NLP
- No external APIs
- Designed to satisfy challenge runtime constraints



# Key Features

- Explainable ranking decisions
- Semantic candidate matching
- Behavioral signal integration
- Rule-based profile validation
- Efficient streaming data processing
- CPU-friendly implementation
- Scalable ranking pipeline



# Future Improvements

- Sentence Transformer embeddings
- Learning-to-Rank models
- Cross-Encoder reranking
- Personalized recruiter preferences
- Online feedback learning
- Adaptive score calibration


Developed as part of the **Redrob AI Intelligent Candidate Discovery & Ranking Challenge**.
