"""
modules/reimbursement/sheets_service.py

Handles all Google Sheets operations for the reimbursement system:
  - Appending a new expense submission row to the tracker sheet
"""

import os
from datetime import datetime

# Import the unified Google API service builder
from core import get_service

# Column order in Sheet1: Date | Name | Team | Purpose | Place | Total | Drive Link
SHEET_RANGE = 'Sheet1!A:G'

def append_to_sheet(data: dict) -> dict:
    """
    Appends one row of expense data to the Google Sheet tracker.
    
    Args:
        data (dict): A dictionary containing the submission details.
                     Expected keys: 'employeeName', 'team', 'purpose', 
                     'place', 'totalExpense', 'driveLink'.
                     
    Returns:
        dict: The response from the Google Sheets API.
    """
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    
    if not sheet_id:
        raise ValueError("CRITICAL: GOOGLE_SHEET_ID is missing from the .env file.")

    # Format the current date as MM/DD/YYYY (matching JS toLocaleDateString default)
    current_date = datetime.now().strftime("%m/%d/%Y")

    # Construct the row array in the exact order the sheet expects
    row = [
        current_date,
        data.get('employeeName', ''),
        data.get('team', ''),
        data.get('purpose', ''),
        data.get('place', ''),
        data.get('totalExpense', 0),
        data.get('driveLink', '')
    ]

    try:
        # Build the Sheets service using the unified authentication
        sheets_service = get_service('sheets', 'v4')
        
        # Execute the append request
        response = sheets_service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range=SHEET_RANGE,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': [row]}
        ).execute()
        
        return response
        
    except Exception as e:
        raise RuntimeError(f"Failed to append data to Google Sheets: {e}")