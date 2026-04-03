from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_cosine(text1, text2):
    if not text1.strip() or not text2.strip():
        return 0.0

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]


def compute_scores(cv_data, jobs):
    results = []

    for job in jobs:
        job_id = job.get("job_id", None)
        title = job.get("title", "")
        description = job.get("description", "")

        # combine title + description for richer matching
        job_text = f"{title} {description}".lower().strip()

        full_score = compute_cosine(cv_data["full_text"], job_text)
        skills_score = compute_cosine(cv_data["skills"], job_text)
        languages_score = compute_cosine(cv_data["languages"], job_text)

        final_score = (
            0.5 * full_score +
            0.3 * skills_score +
            0.2 * languages_score
        )

        results.append({
            "job_id": job_id,
            "title": title,
            "final_score": float(final_score),
            "details": {
                "full": float(full_score),
                "skills": float(skills_score),
                "languages": float(languages_score)
            }
        })

    return results


def rank_results(results):
    return sorted(results, key=lambda x: x["final_score"], reverse=True)