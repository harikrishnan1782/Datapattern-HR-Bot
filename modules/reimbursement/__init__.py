"""
modules/reimbursement/__init__.py

Initializes the Expense Reimbursement module.
Exposes the core Google Workspace service functions (Drive, Sheets, Gmail) 
required to process reimbursement submissions from the main app.

Usage example in app.py:
    from modules.reimbursement import resolve_destination_folder, upload_file_to_drive, append_to_sheet, send_alert_email
"""

from .drive_service import resolve_destination_folder, upload_file_to_drive
from .sheets_service import append_to_sheet
from .gmail_service import send_alert_email

# Explicitly define the public API of this module
__all__ = [
    "resolve_destination_folder",
    "upload_file_to_drive",
    "append_to_sheet",
    "send_alert_email"
]