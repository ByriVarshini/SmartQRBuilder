import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import urllib.parse

def generate_qr():
    qr_type = qr_type_var.get()
    data = entry.get()

    if qr_type in ["Link", "Email"] and not data:
        messagebox.showwarning("Input Error", "Please enter data to generate QR code.")
        return

    if qr_type == "Link":
        qr_data = data
    elif qr_type == "Email":
        qr_data = f"mailto:{data}"
    elif qr_type == "Contact Info":
        open_contact_popup()
        return
    elif qr_type == "UPI Payment":
        open_upi_popup()
        return
    else:
        qr_data = data

    show_qr(qr_data)

def show_qr(qr_data):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save("temp_qr.png")

    img_display = Image.open("temp_qr.png")
    img_display = img_display.resize((200, 200), Image.Resampling.LANCZOS)
    img_display = ImageTk.PhotoImage(img_display)

    qr_label.config(image=img_display)
    qr_label.image = img_display

def save_qr():
    if not entry.get() and qr_type_var.get() not in ["Contact Info", "UPI Payment"]:
        messagebox.showinfo("No QR Code", "Please generate a QR code first.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png")])
    if file_path:
        qr_type = qr_type_var.get()
        data = entry.get()

        if qr_type == "Link":
            qr_data = data
        elif qr_type == "Email":
            qr_data = f"mailto:{data}"
        else:
            messagebox.showinfo("Save Unavailable", "Please generate and save this QR through the popup.")
            return

        qr = qrcode.make(qr_data)
        qr.save(file_path)
        messagebox.showinfo("Saved", f"QR Code saved to:\n{file_path}")

def open_contact_popup():
    contact_window = tk.Toplevel(root)
    contact_window.title("Contact Details")
    contact_window.geometry("300x350")
    contact_window.resizable(False, False)

    tk.Label(contact_window, text="First Name").pack(pady=3)
    first_name = tk.Entry(contact_window, width=30)
    first_name.pack()

    tk.Label(contact_window, text="Last Name").pack(pady=3)
    last_name = tk.Entry(contact_window, width=30)
    last_name.pack()

    tk.Label(contact_window, text="Phone Number").pack(pady=3)
    phone = tk.Entry(contact_window, width=30)
    phone.pack()

    tk.Label(contact_window, text="Email").pack(pady=3)
    email = tk.Entry(contact_window, width=30)
    email.pack()

    tk.Label(contact_window, text="Organization").pack(pady=3)
    org = tk.Entry(contact_window, width=30)
    org.pack()

    def submit_contact():
        fn = first_name.get()
        ln = last_name.get()
        tel = phone.get()
        mail = email.get()
        orgn = org.get()

        if not fn and not ln:
            messagebox.showwarning("Missing Info", "Please enter at least the first or last name.")
            return

        vcard_data = f"""BEGIN:VCARD
VERSION:3.0
N:{ln};{fn}
FN:{fn} {ln}
ORG:{orgn}
TEL:{tel}
EMAIL:{mail}
END:VCARD"""

        contact_window.destroy()
        show_qr(vcard_data)

    tk.Button(contact_window, text="Generate QR", command=submit_contact, bg="#4CAF50", fg="white").pack(pady=15)

def open_upi_popup():
    upi_window = tk.Toplevel(root)
    upi_window.title("UPI Payment Details")
    upi_window.geometry("300x250")
    upi_window.resizable(False, False)

    tk.Label(upi_window, text="UPI ID").pack(pady=3)
    upi_id_entry = tk.Entry(upi_window, width=30)
    upi_id_entry.pack()

    tk.Label(upi_window, text="Name").pack(pady=3)
    name_entry = tk.Entry(upi_window, width=30)
    name_entry.pack()

    tk.Label(upi_window, text="Amount (optional)").pack(pady=3)
    amount_entry = tk.Entry(upi_window, width=30)
    amount_entry.pack()

    def submit_upi():
        upi_id = upi_id_entry.get()
        name = name_entry.get()
        amount = amount_entry.get()

        if not upi_id or not name:
            messagebox.showwarning("Missing Info", "Please enter UPI ID and Name.")
            return

        # URL encode the name for safety
        name_encoded = urllib.parse.quote(name)

        upi_data = f"upi://pay?pa={upi_id}&pn={name_encoded}"
        if amount:
            upi_data += f"&am={amount}&cu=INR"

        upi_window.destroy()
        show_qr(upi_data)

    tk.Button(upi_window, text="Generate QR", command=submit_upi, bg="#4CAF50", fg="white").pack(pady=15)

def update_input_field(*args):
    selected_type = qr_type_var.get()
    if selected_type in ["Contact Info", "UPI Payment"]:
        entry_label.pack_forget()
        entry.pack_forget()
    else:
        entry_label.pack(pady=5)
        entry.pack(pady=10)

# GUI Setup
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x500")
root.resizable(False, False)

tk.Label(root, text="Select QR Code Type", font=("Arial", 12)).pack(pady=5)

qr_type_var = tk.StringVar(value="Link")
qr_type_var.trace("w", update_input_field)

qr_types = ["Link", "Email", "Contact Info", "UPI Payment"]  # "Amount (INR)" removed
dropdown = tk.OptionMenu(root, qr_type_var, *qr_types)
dropdown.config(width=20, font=("Arial", 11))
dropdown.pack(pady=5)

entry_label = tk.Label(root, text="Enter Data", font=("Arial", 14))
entry_label.pack(pady=5)

entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=10)

tk.Button(root, text="Generate QR Code", command=generate_qr, bg="#4CAF50", fg="white", width=20).pack(pady=10)
tk.Button(root, text="Save QR Code", command=save_qr, bg="#2196F3", fg="white", width=20).pack(pady=5)

qr_label = tk.Label(root)
qr_label.pack(pady=20)

root.mainloop()
