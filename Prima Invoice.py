import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import base64

st.set_page_config(page_title="PrimaInvoice", page_icon="🇳🇬", layout="centered")

# === YOUR BANK DETAILS - UPDATE THESE ===
BANK_NAME = "Sterling Bank"                 
ACCOUNT_NUMBER = "0101152030"       
ACCOUNT_NAME = "Emmanuel David"    

# Session state
if 'invoice_count' not in st.session_state:
    st.session_state.invoice_count = 0
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False

# Styling for Install Box (visible in light & dark mode)
st.markdown("""
<style>
    .install-box {
        background-color: #e3f2fd !important;
        color: #0d47a1 !important;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #90caf9;
        margin: 10px 0 20px 0;
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

# Title
st.title("🇳🇬 PrimaInvoice")
st.markdown("<h3 style='text-align: center; color: #1E3A8A;'>Classic Professional Invoices for Nigerian Businesses</h3>", unsafe_allow_html=True)

# Install as App Box - Clearly visible
st.markdown("""
<div class="install-box">
    <h4>📱 Install as App on Your Phone (Free)</h4>
    <p><strong>Android (Chrome):</strong> Tap ⋮ (three dots) → "Add to home screen" or "Install app"</p>
    <p><strong>iPhone (Safari):</strong> Tap Share button → "Add to Home Screen"</p>
    <p><strong>After installing:</strong> Open from home screen like a real app!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
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
    business_name = st.text_input("Your Business Name", "Your Business Name", key="biz_name")
    business_phone = st.text_input("Phone Number", "08012345678", key="biz_phone")
    business_address = st.text_input("Address", "Lagos, Nigeria", key="biz_addr")

# Upgrade Section
if st.session_state.get("show_upgrade", False):
    st.subheader("Upgrade to PrimaInvoice Pro")
    st.write("Pay ₦9,999 to unlock unlimited invoices.")
    
    st.info(f"""
    **Bank Transfer Details:**
    - Bank: **{BANK_NAME}**
    - Account Number: **{ACCOUNT_NUMBER}**
    - Account Name: **{ACCOUNT_NAME}**
    
    **Suggested Narration:** PrimaInvoice Pro - ["DAVID EMMANUEL ENECHE"]
    """)
    
    entered_code = st.text_input("Last 6 digits of transaction ref", placeholder="123456")
    
    if st.button("Activate Pro"):
        if len(entered_code.strip()) >= 4:
            st.session_state.is_pro = True
            st.success("🎉 Pro activated! Unlimited invoices unlocked.")
            st.balloons()
            st.session_state.show_upgrade = False
        else:
            st.error("Please enter at least 4 digits from your transaction reference.")

# Invoice Creator
st.divider()
st.subheader("Create Professional Invoice")

can_create = st.session_state.is_pro or st.session_state.invoice_count < 5

if not can_create:
    st.error("🚫 Free limit reached (5 invoices/month). Upgrade via bank transfer for unlimited!")
else:
    invoice_number = st.text_input("Invoice Number", f"PRI-{datetime.now().strftime('%Y%m%d')}-{st.session_state.invoice_count + 1}")
    customer_name = st.text_input("Customer Name")
    customer_phone = st.text_input("Customer Phone (optional)")

    num_items = st.number_input("Number of Items", min_value=1, value=1, step=1)
    items = []
    total = 0.0

    for i in range(int(num_items)):
        col1, col2, col3 = st.columns([3, 1.5, 1.5])
        with col1:
            desc = st.text_input(f"Item {i+1} Description", key=f"desc_{i}")
        with col2:
            qty = st.number_input("Qty", min_value=1, value=1, key=f"qty_{i}")
        with col3:
            price = st.number_input("Price ₦", min_value=0, value=5000, key=f"price_{i}")
        subtotal = qty * price
        total += subtotal
        items.append({"desc": desc or "Item", "qty": qty, "price": price, "subtotal": subtotal})

    vat = total * 0.075
    grand_total = total + vat

    st.write(f"**Subtotal:** ₦{total:,.0f}")
    st.write(f"**VAT (7.5%):** ₦{vat:,.0f}")
    st.write(f"**Grand Total:** ₦{grand_total:,.0f}")

    if st.button("Generate & Download PDF", type="primary"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # PDF Header
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, height - 80, "PrimaInvoice")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 100, business_name)
        c.drawString(50, height - 120, business_phone)
        c.drawString(50, height - 140, business_address)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 200, f"Invoice #{invoice_number}")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 220, f"Date: {datetime.now().strftime('%d %B %Y')}")
        c.drawString(50, height - 240, f"Customer: {customer_name}")
        if customer_phone:
            c.drawString(50, height - 260, f"Phone: {customer_phone}")

        # Items Table
        y = height - 320
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Description")
        c.drawString(300, y, "Qty")
        c.drawString(380, y, "Unit Price")
        c.drawString(480, y, "Amount")

        y -= 25
        c.setFont("Helvetica", 11)
        for item in items:
            c.drawString(50, y, str(item["desc"])[:40])
            c.drawString(300, y, str(item["qty"]))
            c.drawString(380, y, f"₦{item['price']:,.0f}")
            c.drawString(480, y, f"₦{item['subtotal']:,.0f}")
            y -= 20

        # Totals
        c.drawString(380, y-30, "Subtotal")
        c.drawString(480, y-30, f"₦{total:,.0f}")
        c.drawString(380, y-50, "VAT 7.5%")
        c.drawString(480, y-50, f"₦{vat:,.0f}")
        c.setFont("Helvetica-Bold", 14)
        c.drawString(380, y-80, "TOTAL DUE")
        c.drawString(480, y-80, f"₦{grand_total:,.0f}")

        c.save()
        buffer.seek(0)

        b64 = base64.b64encode(buffer.read()).decode()
        st.success("✅ Professional invoice generated!")
        st.download_button(
            "⬇️ Download PDF Invoice",
            data=base64.b64decode(b64),
            file_name=f"{invoice_number}.pdf",
            mime="application/pdf"
        )

        st.session_state.invoice_count += 1
        if not st.session_state.is_pro:
            st.info(f"Free invoices used: {st.session_state.invoice_count}/5 this month")

st.divider()
st.caption("PrimaInvoice – Classic. Professional. Built for Nigerian businesses. Pro unlocks unlimited use.")
