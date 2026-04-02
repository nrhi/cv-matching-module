import re
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


IMPORTANT_WORDS = [
    "python", "django", "sql", "api", "machine", "learning",
    "anglais", "français", "italien", "langues", "traduction",
    "communication", "service", "client", "accueil", "relationnel",
    "travail", "équipe", "créativité", "ponctualité", "photoshop",
    "montage", "vidéo", "bénévole", "stage", "étudiant", "hôtel"
]


def extract_cv_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s+#./-]", "", text)
    return text.strip()


def filter_important(text, keywords):
    words = text.split()
    filtered = [word for word in words if word in keywords]
    return " ".join(filtered)


def compute_cosine_scores(cv_text, job_descriptions):
    documents = [cv_text] + job_descriptions

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    cv_vector = tfidf_matrix[0:1]
    job_vectors = tfidf_matrix[1:]

    scores = cosine_similarity(cv_vector, job_vectors)[0]
    return scores


def rank_jobs(scores):
    job_scores = list(enumerate(scores, start=1))
    return sorted(job_scores, key=lambda x: x[1], reverse=True)


def save_results(results, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for job_id, score in results:
            f.write(f"Job {job_id}: {score:.4f}\n")


# 🚀 MAIN EXECUTION
if __name__ == "__main__":

    pdf_path = "../data/sample_cv.pdf"

    job_descriptions = [
        "Nous recherchons une étudiante avec un bon sens relationnel, le travail en équipe, l'accueil et le service client pour un poste d'hôtesse d'accueil dans un hôtel.",
        "Nous recrutons un développeur Python avec Django, SQL, API et expérience en machine learning.",
        "Stage en traduction et langues étrangères. Le candidat doit parler français, anglais et italien et avoir de bonnes compétences en communication."
    ]

    raw_text = extract_cv_text(pdf_path)
    cleaned_text = clean_text(raw_text)

    cv_filtered = filter_important(cleaned_text, IMPORTANT_WORDS)
    filtered_jobs = [filter_important(job.lower(), IMPORTANT_WORDS) for job in job_descriptions]

    scores_keywords = compute_cosine_scores(cv_filtered, filtered_jobs)
    scores_full = compute_cosine_scores(cleaned_text, [job.lower() for job in job_descriptions])

    print("Keyword-based scores:")
    for i, score in enumerate(scores_keywords, start=1):
        print(f"Job {i}: {score:.4f}")

    print("\nFull-text scores:")
    for i, score in enumerate(scores_full, start=1):
        print(f"Job {i}: {score:.4f}")

    ranked = rank_jobs(scores_keywords)

    print("\nRanked jobs:")
    for job_id, score in ranked:
        print(f"Job {job_id}: {score:.4f}")

    save_results(ranked, "../outputs/final_ranked_jobs.txt")
    print("\nResults saved successfully!")