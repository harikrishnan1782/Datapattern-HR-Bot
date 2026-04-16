import base64
import re
from email.message import EmailMessage

# Import the unified Google API service builder
from core.google_auth import get_service
from .email_template import build_email_html, build_email_plain

def is_valid_email(email: str) -> bool:
    """Validates the email string using regex."""
    pattern = r"^[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-.]+$"
    return bool(re.match(pattern, email.strip()))

def dispatch_offer_email(
    recipient_email: str,
    cc_email: str,
    candidate_name: str,
    role: str,
    docx_bytes: bytes,
    filename: str,
    sender_email: str,
) -> dict:
    
    if not is_valid_email(recipient_email):
        return {"success": False, "message": "Invalid recipient email address format."}

    if not sender_email.strip() or not is_valid_email(sender_email.strip()):
        return {"success": False, "message": "Invalid sender email address format."}

    # ── Safely format CCs ──
    cc_list = []
    if cc_email.strip():
        raw_ccs = [e.strip() for e in cc_email.replace(";", ",").split(",") if e.strip()]
        for cc in raw_ccs:
            if is_valid_email(cc):
                cc_list.append(cc)
            else:
                return {"success": False, "message": f"Invalid CC email format detected: {cc}"}

    # 1. Build the base EmailMessage
    msg = EmailMessage()
    msg["From"] = f"DataPattern HR <{sender_email.strip()}>"
    msg["To"] = recipient_email.strip()
    msg["Subject"] = f"Offer Letter — {role} at DataPattern"
    
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    # 2. Add the email body (Plain text fallback + HTML content)
    plain_text = build_email_plain(candidate_name, role)
    html_text = build_email_html(candidate_name, role)
    
    msg.set_content(plain_text)
    msg.add_alternative(html_text, subtype='html')

    # 3. Attach the DOCX file (directly from bytes)
    msg.add_attachment(
        docx_bytes, 
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.wordprocessingml.document", 
        filename=filename
    )

    # 4. Encode the message into the base64 payload Gmail expects
    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
    create_message = {'raw': raw_message}
    
    # 5. Send via the unified Google Auth service
    try:
        service = get_service('gmail', 'v1')
        service.users().messages().send(userId="me", body=create_message).execute()
        
        return {
            "success": True,
            "message": f"Email dispatched successfully to **{recipient_email}**"
        }
    except Exception as e:
        return {"success": False, "message": f"API Error: {e}"}