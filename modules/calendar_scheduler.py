from datetime import datetime, timedelta
import os.path
from pathlib import Path
import uuid

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define absolute paths based on the directory structure
BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

# Calendar permissions
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    """Authenticates the user and returns the Google Calendar API service using absolute file paths."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("BASE_DIR =", BASE_DIR)
            print("CREDENTIALS_FILE =", CREDENTIALS_FILE)
            print("Exists =", CREDENTIALS_FILE.exists())

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service


def schedule_interview(
    candidate_name,
    candidate_email,
    interview_date,
    interview_time,
):
    """Schedules a Google Calendar event with a Google Meet link."""
    service = get_calendar_service()

    # Convert Streamlit date & time into datetime
    start = datetime.combine(interview_date, interview_time)
    end = start + timedelta(hours=1)

    event_body = {
        "summary": f"Interview - {candidate_name}",
        "description": "AI Candidate Screening Interview",
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "attendees": [
            {"email": candidate_email},
        ],
        "conferenceData": {
            "createRequest": {
                "requestId": str(uuid.uuid4()),
                "conferenceSolutionKey": {
                    "type": "hangoutsMeet"
                },
            }
        },
    }

    event = (
        service.events()
        .insert(
            calendarId="primary",
            body=event_body,
            conferenceDataVersion=1,
            sendUpdates="all",
        )
        .execute()
    )

    # Safely retrieve the Google Meet link
    meet_link = None
    conference_data = event.get("conferenceData", {})
    entry_points = conference_data.get("entryPoints", [])

    for entry in entry_points:
        if entry.get("entryPointType") == "video":
            meet_link = entry.get("uri")
            break

    return meet_link or event.get("htmlLink")