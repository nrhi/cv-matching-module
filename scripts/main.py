from cv_reader import read_cv
from cv_cleaner import clean_text
from cv_sections import extract_sections
from cv_matcher import compute_scores, rank_results

import json
import os
import csv


# =========================
# LOAD JOBS (CSV OR JSON)
# =========================

def load_jobs_from_csv(path):
    jobs = []

    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # 🔥 CLEAN HEADERS
        reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]
        print("CLEANED CSV columns:", reader.fieldnames)

        for i, row in enumerate(reader, start=1):

            # normalize row keys too
            row = {k.strip().lower(): v for k, v in row.items()}

            job_id = row.get("job_id") or row.get("id") or i

            title = row.get("title", "Untitled Job")

            description = (
                row.get("description")
                or row.get("descriptio")   # your broken column
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

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        print("CSV columns found:", reader.fieldnames)

        for i, row in enumerate(reader, start=1):

            # robust job_id
            job_id = (
                row.get("job_id")
                or row.get("id")
                or i
            )

            # 🔥 FIXED TITLE (your CSV uses "title")
            title = next(
                (row[key] for key in row if key.strip().lower() == "title"),
                "Untitled Job"
            )

            # 🔥 FIXED DESCRIPTION (your CSV has typo like "descriptio")
            description = next(
                (row[key] for key in row if "descript" in key.strip().lower()),
                ""
            )

            # optional fields
            location = next(
                (row[key] for key in row if "location" in key.lower()),
                ""
            )

            company = next(
                (row[key] for key in row if "company" in key.lower()),
                ""
            )

            jobs.append({
                "job_id": int(job_id) if str(job_id).isdigit() else i,
                "title": title,
                "description": description,
                "location": location,
                "company": company
            })

    return jobs


def load_jobs(jobs_file):
    if jobs_file.endswith(".csv"):
        return load_jobs_from_csv(jobs_file)

    elif jobs_file.endswith(".json"):
        with open(jobs_file, "r", encoding="utf-8") as f:
            return json.load(f)

    else:
        raise ValueError("Unsupported jobs file type")


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

jobs_file = "../data/jobs.csv"
jobs = load_jobs(jobs_file)

data_folder = "../data"

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