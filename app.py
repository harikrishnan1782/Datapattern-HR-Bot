"""
app.py

Main Entry Point for the DataPattern HR Automation Agent.
Unifies the Offer Letter Generator and the Expense Reimbursement System 
into a single, robust Streamlit interface.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Import our modularized UI components
from ui import render_offer_tab, render_reimburse_tab

# Load environment variables (Unified Auth)
load_dotenv()

# ==========================================
# PAGE CONFIGURATION & INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="DataPattern · HR Automation Agent",
    page_icon="🏢",
    layout="wide"
)

# Load Custom CSS
CSS_PATH = os.path.join("assets", "styles.css")
if os.path.exists(CSS_PATH):
    with open(CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Session State for Offer Letters
if "generated_bytes" not in st.session_state:
    st.session_state.generated_bytes = None
if "generated_name" not in st.session_state:
    st.session_state.generated_name = ""
if "preview_data" not in st.session_state:
    st.session_state.preview_data = {}

# Load Offer Letter Template
TEMPLATE_PATH = os.path.join("modules", "offer_letter", "DataPattern Offer Letter_sample.docx")
def load_template():
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "rb") as f:
            return f.read()
    return None

template_bytes = load_template()

# ==========================================
# MAIN UI ROUTING
# ==========================================
st.title("DataPattern HR Automation Agent 🏢")
st.markdown("One unified portal for generating offer letters and processing expense reimbursements.")
st.markdown("---")

# Setup the main tabs
tab_offer, tab_reimburse = st.tabs(["📝 Offer Letter Generator", "💸 Expense Reimbursement"])

with tab_offer:
    render_offer_tab(template_bytes)

with tab_reimburse:
    render_reimburse_tab()