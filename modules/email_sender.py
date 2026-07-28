import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read email credentials
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(receiver_email, candidate_name, test_link):
    """
    Send a technical assessment email to a candidate.
    """

    msg = EmailMessage()

    msg["Subject"] = "Technical Assessment Invitation"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email

    msg.set_content(f"""
Dear {candidate_name},

Congratulations!

Based on your resume and GitHub profile, you have been shortlisted for the next stage of our recruitment process.

Please complete the technical assessment using the link below:

{test_link}

Kindly complete the assessment before the deadline.

Best Regards,
HR Team
""")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")


# Test the email sender
if __name__ == "__main__":

    print("Email:", EMAIL_ADDRESS)
    print("Password Loaded:", EMAIL_PASSWORD is not None)
    print("Password Length:", len(EMAIL_PASSWORD) if EMAIL_PASSWORD else 0)

    send_email(
        receiver_email="adityashukla5177@gmail.com",
        candidate_name="Aditya",
        test_link="https://forms.gle/demo123"
    )