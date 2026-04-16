"""
core/google_auth.py

Unified Google API Authentication Module.
Reconstructs Google OAuth2 credentials dynamically using the Refresh Token 
stored in the .env file, enabling headless server deployment.
"""

import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load environment variables from the .env file
load_dotenv()

# Consolidated scopes needed for both apps:
# 1. Drive (Uploading PDFs)
# 2. Sheets (Tracking reimbursement submissions)
# 3. Gmail (Sending HR alerts and Offer Letters)
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.send"
]

def get_google_credentials() -> Credentials:
    """
    Builds Google OAuth2 credentials directly from .env variables.
    The 'token=None' parameter forces the google-auth library to 
    automatically fetch a fresh access token using the refresh_token.
    """
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")

    # Guard clause to catch missing environment variables early
    if not all([client_id, client_secret, refresh_token]):
        raise ValueError(
            "CRITICAL ERROR: Missing Google OAuth credentials. "
            "Ensure GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REFRESH_TOKEN "
            "are properly set in your .env file."
        )

    return Credentials(
        token=None, 
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES
    )

def get_service(api_name: str, api_version: str):
    """
    Builds and returns the requested Google API service client.
    
    Usage Examples:
        drive_service = get_service('drive', 'v3')
        sheets_service = get_service('sheets', 'v4')
        gmail_service = get_service('gmail', 'v1')
        
    Args:
        api_name (str): The name of the API (e.g., 'gmail', 'drive', 'sheets').
        api_version (str): The version of the API (e.g., 'v1', 'v3', 'v4').
        
    Returns:
        Resource: The constructed Google API service client.
    """
    try:
        creds = get_google_credentials()
        # The build() method caches discovery documents to speed up execution
        service = build(api_name, api_version, credentials=creds)
        return service
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Google API service '{api_name} {api_version}': {str(e)}")