"""
ui/reimburse_tab.py

Handles the Streamlit UI layout and interactions for the Expense Reimbursement tab.
"""

import time
import streamlit as st
from modules.reimbursement import (
    resolve_destination_folder, 
    upload_file_to_drive, 
    append_to_sheet, 
    send_alert_email
)

def render_reimburse_tab():
    st.subheader("Submit Travel & Business Expenses")
    
    with st.form("reimbursement_form", clear_on_submit=True):
        st.markdown("#### Employee Information")
        col1, col2 = st.columns(2)
        emp_name = col1.text_input("Employee Name *")
        emp_email = col2.text_input("Employee Email *")
        
        col3, col4, col5 = st.columns(3)
        team = col3.selectbox("Team *", ["Data Engineering", "Gen AI", "Sales", "HR", "Pre Sales"])
        purpose = col4.text_input("Purpose of Visit *")
        place = col5.text_input("Place of Visit *")
        
        st.markdown("#### Travel Dates")
        d1, d2 = st.columns(2)
        from_date = d1.date_input("From Date *")
        to_date = d2.date_input("To Date *")
        
        st.markdown("#### Expense Details")
        st.info("Edit the table below to add your expenses. Click the '+' sign at the bottom of the table to add more rows.")
        
        # Interactive Data Editor replacing the clunky JavaScript row additions
        default_grid = [{"Expenditure": "", "Bill No / GSTIN": "", "Amount (Rs.)": 0.0}]
        expense_df = st.data_editor(default_grid, num_rows="dynamic", use_container_width=True)
        
        st.markdown("#### Receipt Upload")
        receipt_file = st.file_uploader("Consolidated Bills (PDF only) *", type=["pdf"])
        
        submitted = st.form_submit_button("Submit Reimbursement", type="primary", use_container_width=True)
        
        if submitted:
            # 1. Validation
            if not emp_name or not team or not purpose or not receipt_file:
                st.error("⚠️ Please fill in all required fields and upload the PDF receipt.")
            else:
                # Calculate total from the dynamic grid
                total_expense = sum(float(row.get("Amount (Rs.)", 0)) for row in expense_df)
                
                if total_expense <= 0:
                    st.error("⚠️ Total expense must be greater than 0.")
                else:
                    with st.status("Processing Reimbursement Pipeline...", expanded=True) as status:
                        try:
                            # Phase 1: Google Drive
                            st.write("📁 Resolving Drive folders and uploading PDF...")
                            formatted_date = from_date.strftime("%Y-%m-%d")
                            folder_id = resolve_destination_folder(team, formatted_date)
                            
                            file_name = f"{emp_name.replace(' ', '_')}_Reimbursement_{int(time.time())}.pdf"
                            drive_result = upload_file_to_drive(receipt_file, folder_id, file_name)
                            drive_link = drive_result.get("webViewLink")
                            
                            # Phase 2: Google Sheets
                            st.write("📊 Appending data to Google Sheets Tracker...")
                            sheet_data = {
                                "employeeName": emp_name,
                                "team": team,
                                "purpose": purpose,
                                "place": place,
                                "totalExpense": total_expense,
                                "driveLink": drive_link
                            }
                            append_to_sheet(sheet_data)
                            
                            # Phase 3: Gmail HR Alert
                            st.write("📧 Sending alert notification to HR...")
                            send_alert_email(emp_name, team, total_expense)
                            
                            status.update(label="Reimbursement Successfully Processed!", state="complete", expanded=False)
                            st.success(f"Success! Rs. {total_expense} tracked, PDF uploaded, and HR Notified.")
                            
                        except Exception as e:
                            status.update(label="Pipeline Failed", state="error")
                            st.error(f"An error occurred during processing: {str(e)}")