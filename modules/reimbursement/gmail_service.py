"""
modules/reimbursement/gmail_service.py

Handles all Gmail operations for the reimbursement system:
  - Sending a plain-text alert email to HR when a new submission is received
"""

import os
import base64
from email.mime.text import MIMEText

# Import the unified Google API service builder
from core import get_service

def send_alert_email(employee_name: str, team: str, total_expense: float | str) -> dict:
    """
    Sends an HR alert email notifying them of a new expense submission.
    
    Args:
        employee_name: Name of the employee claiming reimbursement.
        team: The employee's team/department.
        total_expense: The total amount claimed.
        
    Returns:
        dict: A success status and message.
    """
    hr_email = os.getenv("HR_EMAIL")
    
    if not hr_email:
        raise ValueError("CRITICAL: HR_EMAIL is missing from the .env file.")

    # 1. Construct the Subject and Body
    subject = f"New Expense Reimbursement: {employee_name} - {team}"
    
    body_text = (
        "Hello HR Team,\n\n"
        "A new expense reimbursement request has been submitted.\n\n"
        "Details:\n"
        f"  Employee : {employee_name}\n"
        f"  Team     : {team}\n"
        f"  Amount   : Rs. {total_expense}\n\n"
        "Please check the Google Sheet Tracker to review the full breakdown "
        "and access the receipt PDF.\n\n"
        "Best regards,\n"
        "Automated Reimbursement System"
    )

    # 2. Build the MIME object
    message = MIMEText(body_text)
    message["To"] = hr_email
    message["Subject"] = subject

    # 3. base64url-encode the message as required by the Gmail API
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # 4. Dispatch via unified Google Auth
    try:
        gmail_service = get_service('gmail', 'v1')
        
        gmail_service.users().messages().send(
            userId="me", 
            body={'raw': raw_message}
        ).execute()
        
        return {"success": True, "message": "HR Alert email dispatched successfully."}
        
    except Exception as e:
        raise RuntimeError(f"Failed to send HR alert email: {e}")