"""
modules/reimbursement/drive_service.py

Handles all Google Drive operations for the reimbursement system:
  - Finding or creating nested folders (team / year / month)
  - Uploading PDF receipts directly from Streamlit memory
"""

import os
import io
from datetime import datetime
from googleapiclient.http import MediaIoBaseUpload

# Import the unified Google API service builder
from core import get_service

def check_and_create_folder(folder_name: str, parent_id: str) -> str:
    """
    Searches for a folder by name inside a parent folder.
    Creates the folder if it does not exist.
    """
    drive_service = get_service('drive', 'v3')

    # Query to find exactly this folder within the specified parent
    query = (
        f"name='{folder_name}' and "
        f"'{parent_id}' in parents and "
        f"mimeType='application/vnd.google-apps.folder' and "
        f"trashed=false"
    )

    response = drive_service.files().list(
        q=query,
        fields='files(id, name)',
        spaces='drive',
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()

    files = response.get('files', [])

    # If folder exists, return its ID
    if files:
        return files[0]['id']

    # If it doesn't exist, create it
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }

    folder = drive_service.files().create(
        body=folder_metadata,
        fields='id',
        supportsAllDrives=True
    ).execute()

    return folder.get('id')


def resolve_destination_folder(team: str, from_date: str) -> str:
    """
    Resolves or creates the full folder path for a submission:
    Root > Team > Year > Month
    """
    # Parse the date string (Expected format from HTML5 input: YYYY-MM-DD)
    date_obj = datetime.strptime(from_date, "%Y-%m-%d")
    year = str(date_obj.year)
    month = date_obj.strftime("%B")  # Full month name (e.g., 'January')
    
    root_folder_id = os.getenv("DRIVE_ROOT_FOLDER_ID")
    
    if not root_folder_id:
        raise ValueError("DRIVE_ROOT_FOLDER_ID is missing from the .env file.")

    # Recursively resolve/create the path down to the specific month
    team_folder_id = check_and_create_folder(team, root_folder_id)
    year_folder_id = check_and_create_folder(year, team_folder_id)
    month_folder_id = check_and_create_folder(month, year_folder_id)

    return month_folder_id


def upload_file_to_drive(file_obj, parent_folder_id: str, new_file_name: str) -> dict:
    """
    Uploads a Streamlit UploadedFile object to the specified Google Drive folder.
    
    Args:
        file_obj: The file object from Streamlit's st.file_uploader.
        parent_folder_id: Drive ID of the destination folder.
        new_file_name: The name to save the file as in Drive.
        
    Returns:
        dict: Containing the 'id' and 'webViewLink' of the uploaded file.
    """
    drive_service = get_service('drive', 'v3')

    file_metadata = {
        'name': new_file_name,
        'parents': [parent_folder_id]
    }

    # Streamlit files are kept in memory; we wrap the bytes for the Google API
    media = MediaIoBaseUpload(
        io.BytesIO(file_obj.getvalue()), 
        mimetype="application/pdf", 
        resumable=True
    )

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink',
        supportsAllDrives=True
    ).execute()

    return uploaded_file