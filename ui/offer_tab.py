"""
ui/offer_tab.py

Handles the Streamlit UI layout and interactions for the Offer Letter Generator tab.
"""

import streamlit as st
from modules.offer_letter import generate_offer_letter, dispatch_offer_email

def render_offer_tab(template_bytes):
    if not template_bytes:
        st.error("⚠️ Template not found. Please ensure the 'DataPattern Offer Letter_sample.docx' file exists in the modules/offer_letter/ directory.")
        return

    # Use sub-tabs to keep the original 3-step workflow clean
    sub_gen, sub_send, sub_preview = st.tabs(["1. Generate Letter", "2. Send Email", "3. Preview"])
    
    # --- Step 1: Generate ---
    with sub_gen:
        st.subheader("Candidate Details")
        c1, c2 = st.columns([1, 3])
        title = c1.selectbox("Title", ["Mr.", "Ms.", "Mrs.", "Dr."])
        cand_name = c2.text_input("Full Name *", placeholder="e.g. Arjun Sharma")
        
        c3, c4 = st.columns(2)
        role = c3.text_input("Role / Designation *", placeholder="e.g. Data Analyst")
        offer_date = c4.text_input("Offer Date", placeholder="e.g. 06 Apr 2026")
        
        c5, c6 = st.columns(2)
        joining_date = c5.text_input("Joining Date", placeholder="e.g. 01 May 2026")
        location = c6.text_input("Location", placeholder="e.g. Coimbatore")
        
        if st.button("⚡ Generate Offer Letter", type="primary"):
            if not cand_name or not role:
                st.warning("Please fill in Candidate Name and Role.")
            else:
                with st.spinner("Personalising offer letter..."):
                    result = generate_offer_letter(
                        template_bytes=template_bytes,
                        title=title, name=cand_name, role=role,
                        offer_date=offer_date, joining_date=joining_date,
                        location=location, phone="", address="", 
                        hr_name="HR Team", hr_dept="Human Resources"
                    )
                    if result["success"]:
                        st.session_state.generated_bytes = result["bytes"]
                        st.session_state.generated_name = result["filename"]
                        st.session_state.preview_data = result["preview_data"]
                        st.success(f"✅ Offer letter ready for **{result['full_name']}**!")
                    else:
                        st.error(f"Generation failed: {result['error']}")
        
        if st.session_state.generated_bytes:
            st.download_button(
                "⬇️ Download Generated DOCX", 
                data=st.session_state.generated_bytes, 
                file_name=st.session_state.generated_name
            )

    # --- Step 2: Send Email ---
    with sub_send:
        st.subheader("Dispatch via Email")
        sender_email = st.text_input("Sender Email *", placeholder="hr@datapattern.ai")
        recipient_email = st.text_input("Recipient Email *", placeholder="candidate@example.com")
        cc_email = st.text_input("CC (optional)", placeholder="ceo@datapattern.ai")
        
        if st.button("🚀 Send Offer Email", type="primary"):
            if not st.session_state.generated_bytes:
                st.warning("Please generate an offer letter first in Step 1.")
            else:
                with st.spinner("Connecting to Gmail API..."):
                    # Use the names from the preview data if available, otherwise use form inputs
                    cname = st.session_state.preview_data.get("Candidate", cand_name)
                    crole = st.session_state.preview_data.get("Role", role)
                    
                    res = dispatch_offer_email(
                        docx_bytes=st.session_state.generated_bytes,
                        filename=st.session_state.generated_name,
                        sender_email=sender_email,
                        recipient_email=recipient_email,
                        cc_email=cc_email,
                        candidate_name=cname,
                        role=crole
                    )
                    if res["success"]:
                        st.success(res["message"])
                        st.balloons()
                    else:
                        st.error(res["message"])

    # --- Step 3: Preview ---
    with sub_preview:
        st.subheader("Offer Summary")
        if not st.session_state.preview_data:
            st.info("No letter generated yet. Please complete Step 1.")
        else:
            for k, v in st.session_state.preview_data.items():
                st.write(f"**{k}:** {v}")