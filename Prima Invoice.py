import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import base64

st.set_page_config(page_title="PrimaInvoice", page_icon="🇳🇬", layout="centered")

# === YOUR BANK DETAILS ===
BANK_NAME = "Sterling Bank"                  
ACCOUNT_NUMBER = "0101152030"       
ACCOUNT_NAME = "Emmanuel David"     

# Session state
if 'invoice_count' not in st.session_state:
    st.session_state.invoice_count = 0
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False

# Better mobile-friendly styling + visible install box in both light and dark mode
st.markdown("""
<style>
    .install-box {
        background-color: #e3f2fd !important;
        color: #0d47a1 !important;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #90caf9;
        margin-bottom: 20px;
        text-align: center;
    }
    @media (prefers-color-scheme: dark) {
        .install-box {
            background-color: #1e3a8a !important;
            color: #e0f2fe !important;
            border-color: #60a5fa;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("🇳🇬 PrimaInvoice")
st.markdown("<h3 style='text-align: center; color: #1E3A8A;'>Professional Invoices for Nigerian Businesses</h3>", unsafe_allow_html=True)

# === INSTALL AS APP BOX (Visible in both Light & Dark Mode) ===
st.markdown("""
<div class="install-box">
    <h4>📱 Install as App on Your Phone (Free & Easy)</h4>
    <p><strong>Android (Chrome):</strong><br>
    1. Tap the three dots ⋮ at the top right<br>
    2. Choose "Add to home screen" or "Install app"</p>
    
    <p><strong>iPhone (Safari):</strong><br>
    1. Tap the Share button (square with arrow)<br>
    2. Scroll down and tap "Add to Home Screen"</p>
    
    <p><strong>After installing:</strong> It will appear on your home screen like a real app!</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Account")
    if st.session_state.is_pro:
        st.success("✅ PRO ACTIVE – Unlimited Invoices")
    else:
        remaining = max(0, 5 - st.session_state.invoice_count)
        st.info(f"Free: {remaining} invoices left this month")

    if not st.session_state.is_pro:
        if st.button("🚀 Upgrade to Pro – ₦9,999/month", type="primary"):
            st.session_state.show_upgrade = True

    st.divider()
    st.subheader("Business Details")
    business_name = st.text_input("Your Business Name", "Prima Invoice", key="biz_name")
    business_phone = st.text_input("Phone Number", "09168489707", key="biz_phone")
    business_address = st.text_input("Address", "Lagos, Nigeria", key="biz_addr")


if st.session_state.get("show_upgrade", False):
    st.subheader("Upgrade to PrimaInvoice Pro")
    st.write("Pay ₦9,999 to unlock unlimited invoices.")
    
    st.info(f"""
    **Bank Transfer Details:**
    - Bank: **{BANK_NAME}**
    - Account Number: **{ACCOUNT_NUMBER}**
    - Account Name: **{ACCOUNT_NAME}**
    
    **Narration:** PrimaInvoice Pro - ["DAVID EMMANUEL ENENCHE"]
    """)
    
    entered_code = st.text_input("Last 6 digits of transaction ref", placeholder="123456")
    
    if st.button("Activate Pro"):
        if len(entered_code.strip()) >= 4:
            st.session_state.is_pro = True
            st.success("🎉 Pro activated! Unlimited invoices unlocked.")
            st.balloons()
            st.session_state.show_upgrade = False
        else:
            st.error("Enter at least 4 digits")

st.divider()
st.caption("PrimaInvoice – Classic. Professional. Built for Nigerian businesses.")
