from cv_reader import read_cv
from cv_cleaner import clean_text
from cv_sections import extract_sections
from cv_matcher import compute_scores, rank_results

import json
import os
import csv


# =========================
# LOAD JOBS
# =========================

def load_jobs_from_csv(path):
    jobs = []

    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # clean headers
        reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]
        print("CSV columns found:", reader.fieldnames)

        for i, row in enumerate(reader, start=1):
            # clean row keys too
            row = {k.strip().lower(): v for k, v in row.items()}

            job_id = row.get("job_id") or row.get("id") or i

            title = row.get("title", "Untitled Job")

            description = (
                row.get("description")
                or row.get("descriptio")
                or row.get("job_description")
                or ""
            )

            location = row.get("location", "")
            company = row.get("company", "")

            jobs.append({
                "job_id": int(job_id) if str(job_id).isdigit() else i,
                "title": title,
                "description": description,
                "location": location,
                "company": company
            })

    return jobs


def load_all_job_files(data_folder):
    all_jobs = []

    for file in os.listdir(data_folder):
        if file.endswith(".csv"):
            csv_path = os.path.join(data_folder, file)
            print(f"Loading jobs from: {file}")
            jobs = load_jobs_from_csv(csv_path)
            all_jobs.extend(jobs)

        elif file.endswith(".json"):
            json_path = os.path.join(data_folder, file)
            print(f"Loading jobs from: {file}")
            with open(json_path, "r", encoding="utf-8") as f:
                jobs = json.load(f)
                all_jobs.extend(jobs)

    return all_jobs


# =========================
# PIPELINE
# =========================

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


# =========================
# SAVE RESULTS
# =========================

def save_results(cv_filename, results):
    output_path = f"../outputs/{cv_filename}_results.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Saved results -> {output_path}")


# =========================
# MAIN
# =========================

data_folder = "../data"
jobs = load_all_job_files(data_folder)

for file in os.listdir(data_folder):

    if file.endswith(".pdf") or file.endswith(".docx"):

        cv_path = os.path.join(data_folder, file)

        print(f"\n====== PROCESSING: {file} ======\n")

        output = run_pipeline(cv_path, jobs)
        results = output["results"]

        for job in results:
            print(f"Job ID: {job['job_id']}")
            print(f"Title: {job['title']}")
            print(f"Final Score: {job['final_score']:.4f}")
            print(f"Details: {job['details']}")
            print()

        filename = file.replace(".pdf", "_pdf").replace(".docx", "_docx")
        save_results(filename, results)