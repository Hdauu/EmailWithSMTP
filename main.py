import smtplib
import schedule
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# ========================
# CONFIGURATION
# ========================

# Your Gmail account
EMAIL = "your_email@gmail.com"

# Gmail password or app password (if 2FA is enabled)
PASSWORD = "your_app_password"

# Recipient address
RECIPIENT = "recipient@example.com"

# Path to the PDF you want to send
PDF_PATH = "file.pdf"

# ========================
# EMAIL SENDING FUNCTION
# ========================

def send_email():
    # Check the current day (Monday = 0, Sunday = 6)
    today = datetime.today().weekday()
    
    # Skip weekends
    if today in [5, 6]:  # Saturday or Sunday
        print("Skipping email: weekend.")
        return

    # Create email content
    subject = "Automated Email with PDF Attachment"
    body = "Hello! This is your scheduled email with a PDF attached."

    # Set up the email structure
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = RECIPIENT
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF file
    try:
        with open(PDF_PATH, 'rb') as f:
            pdf = MIMEApplication(f.read(), _subtype="pdf")
            pdf.add_header('Content-Disposition', 'attachment', filename=PDF_PATH)
            msg.attach(pdf)
    except FileNotFoundError:
        print(f"Error: PDF file '{PDF_PATH}' not found.")
        return

    # Send the email using Gmail's SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# ========================
# DAILY SCHEDULING
# ========================

# Run the job every day at 15:00 UTC (12:00 PM Argentina time)
schedule.every().day.at("15:00").do(send_email)

print("Email bot started. Waiting for the scheduled time...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
