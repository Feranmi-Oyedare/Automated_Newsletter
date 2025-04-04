import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

def send_email():
    # Get the parent directory of the current script
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs', 'Newsletter-Latest-Edition.txt')

    OUTPUT_DIR = os.path.normpath(OUTPUT_DIR)
    if os.path.exists(OUTPUT_DIR):
        with open(OUTPUT_DIR, "r", encoding="utf-8") as f:
            newsletter_content = f.read()

        # create sender's email address
        sender_email = "ayonitemiferanmi@gmail.com"

        # create receiver's email address
        receiver_email = ["feranmi.oyedare@hamoye.org", "oyedare.feranmi@lmu.edu.ng"]

        # create the subject for the message
        subject = "African Authors recognized for their research work"

        # Create Email Message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = ", ".join(receiver_email)  # Multiple recipients
        msg["Subject"] = subject

        # Attach the Email Body
        msg.attach(MIMEText(newsletter_content, "plain", "utf-8"))  # Set encoding to utf-8

        # create the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        # login to the email account
        server.login(user=sender_email, password=os.getenv("GOOGLE_APP_PASSWORD"))

        # send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Email sent out success")
    else:
        print("File not found")
    return "Email sent out successfully!"

if __name__ == "__main__":
    send_email()


