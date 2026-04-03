from cv_reader import read_cv
from cv_cleaner import clean_text
from cv_sections import extract_sections
from cv_matcher import compute_scores, rank_results
import json
import os


# load jobs from JSON
with open("../data/jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)


data_folder = "../data"


def run_pipeline(cv_path, jobs):
    raw_text = read_cv(cv_path)
    cleaned = clean_text(raw_text)
    sections = extract_sections(cleaned)

    cv_data = {
        "full_text": cleaned,
        "skills": sections["skills"],
        "languages": sections["languages"]
    }

    results = compute_scores(cv_data, jobs)
    ranked = rank_results(results)

    return {
        "cv_data": cv_data,
        "results": ranked
    }


# ✅ define FIRST
def save_results(cv_filename, results):
    output_path = f"../outputs/{cv_filename}_results.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Saved results → {output_path}")


# 🔁 LOOP
for file in os.listdir(data_folder):

    if file.endswith(".pdf") or file.endswith(".docx"):

        cv_path = os.path.join(data_folder, file)

        print(f"\n====== PROCESSING: {file} ======\n")

        output = run_pipeline(cv_path, jobs)
        results = output["results"]

        # ✅ print results
        for job in results:
            print(f"Job ID: {job['job_id']}")
            print(f"Title: {job['title']}")
            print(f"Final Score: {job['final_score']:.4f}")
            print()

        # ✅ save results per CV
        filename = file.replace(".", "_")
        save_results(filename, results)