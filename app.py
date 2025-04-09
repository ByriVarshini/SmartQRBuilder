import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO
import urllib.parse

st.set_page_config(page_title="Multi-Purpose QR Code Generator", page_icon="🔳")
st.title("🔳 Multi-Purpose QR Code Generator")

qr_type = st.selectbox("Select QR Code Type", ["Link", "Email", "Contact Info", "UPI Payment"])

qr_data = None  # Final data to encode

# 1. Standard inputs
if qr_type in ["Link", "Email"]:
    user_input = st.text_input("Enter your data")

    if qr_type == "Email" and user_input:
        qr_data = f"mailto:{user_input}"
    elif qr_type == "Link":
        qr_data = user_input

# 2. Contact Info
elif qr_type == "Contact Info":
    st.subheader("Contact Details")
    fn = st.text_input("First Name")
    ln = st.text_input("Last Name")
    tel = st.text_input("Phone Number")
    mail = st.text_input("Email")
    orgn = st.text_input("Organization")

    if fn or ln:
        qr_data = f"""BEGIN:VCARD
VERSION:3.0
N:{ln};{fn}
FN:{fn} {ln}
ORG:{orgn}
TEL:{tel}
EMAIL:{mail}
END:VCARD"""
    else:
        st.warning("Please enter at least a first or last name.")

# 3. UPI Payment
elif qr_type == "UPI Payment":
    st.subheader("UPI Payment Details")
    upi_id = st.text_input("UPI ID")
    name = st.text_input("Name")
    amount = st.text_input("Amount (optional)")

    if upi_id and name:
        name_encoded = urllib.parse.quote(name)
        qr_data = f"upi://pay?pa={upi_id}&pn={name_encoded}"
        if amount:
            qr_data += f"&am={amount}&cu=INR"
    else:
        st.warning("Please enter both UPI ID and Name.")

# Generate QR
if st.button("Generate QR Code") and qr_data:
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to BytesIO for Streamlit
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Show image
    st.image(buffer, caption="Your QR Code")

    # Download button
    st.download_button("Download QR Code", data=buffer.getvalue(), file_name="qr_code.png", mime="image/png")

