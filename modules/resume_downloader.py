import re

def extract_file_id(google_drive_url):
    """
    Extract the file ID from a Google Drive sharing link.
    """

    match = re.search(r"/d/([a-zA-Z0-9_-]+)", google_drive_url)

    if match:
        return match.group(1)

    return None

import requests
import os

def download_resume(google_drive_url, candidate_name):
    """
    Download one resume from Google Drive.
    """

    file_id = extract_file_id(google_drive_url)

    if file_id is None:
        print(f"Invalid URL for {candidate_name}")
        return None

    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(download_url)

    print(response.status_code)
    print(response.headers.get("Content-Type"))

    if response.status_code == 200:

        os.makedirs("resumes", exist_ok=True)

        safe_name = candidate_name.replace(" ", "_")
        file_path = os.path.join("resumes", f"{safe_name}.pdf")

        with open(file_path, "wb") as file:
            file.write(response.content)

        return file_path

    return None

def download_all_resumes(df):
    """
    Download resumes for all candidates in the dataset.
    """

    for index, row in df.iterrows():

        candidate_name = row["name"]
        resume_link = row["resume"]

        print(f"Downloading resume for {candidate_name}...")

        download_resume(resume_link, candidate_name)

    print("All resumes downloaded successfully!")