import base64
from email.mime.text import MIMEText
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
TOKEN_FILE = "token.json"


def _get_credentials(credentials_file: str = "credentials.json") -> Credentials:
    creds = None

    if Path(TOKEN_FILE).exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

        Path(TOKEN_FILE).write_text(creds.to_json(), encoding="utf-8")

    return creds


def create_gmail_draft(
    subject: str,
    body: str,
    to_email: str | None = None,
    credentials_file: str = "credentials.json",
) -> str:
    """
    Create a Gmail draft and return the draft ID.
    """
    creds = _get_credentials(credentials_file=credentials_file)
    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(body, "plain", "utf-8")
    message["subject"] = subject
    if to_email:
        message["to"] = to_email

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    create_message = {"message": {"raw": encoded_message}}

    draft = service.users().drafts().create(userId="me", body=create_message).execute()
    return draft.get("id", "")
