import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("EMAIL_SENDER")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(to_email: str, subject: str, html_body: str) -> None:
    """Helper function to send an HTML email using Gmail SMTP."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    html_part = MIMEText(html_body, "html")
    msg.attach(html_part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())


def send_initial_email(to_email: str, user_name: str, language: str, text: str) -> None:
    """Sends Email #1 containing the reading passage."""
    formatted_text = text.replace("\n", "<br>")

    html_content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #222; max-width: 600px; margin: auto; padding: 20px;">
        <h2 style="color: #1a73e8;">📖 Daily {language} Practice</h2>
        <p style="font-size: 15px;">Hi <strong>{user_name}</strong>,</p>
        <p style="font-size: 14px; color: #555;">
            Read the text below carefully. Try to decipher the meaning and practice reading aloud. 
            Your breakdown and translation will arrive in your inbox in <strong>20 minutes</strong>!
        </p>
        
        <div style="background: #f9f9f9; border-left: 4px solid #1a73e8; padding: 18px; font-size: 19px; margin: 20px 0;">
            {formatted_text}
        </div>
    </div>
    """
    send_email(to_email, f"Daily {language} Reading Practice", html_content)


def send_translation_email(to_email: str, user_name: str, language: str, pronunciation: str, english_translation: str) -> None:
    """Sends Email #2 containing the pronunciation guide and English translation."""
    formatted_pronunciation = pronunciation.replace("\n", "<br>")
    formatted_english = english_translation.replace("\n", "<br>")

    html_content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #222; max-width: 600px; margin: auto; padding: 20px;">
        <h2 style="color: #2e7d32;">✅ {language} Reading Breakdown</h2>
        <p style="font-size: 15px;">Here is the breakdown for today's lesson, <strong>{user_name}</strong>:</p>
        
        <h3 style="color: #333; margin-top: 20px;">Pronunciation / Transliteration</h3>
        <div style="background: #f4fbf4; border-left: 4px solid #2e7d32; padding: 15px; font-size: 16px; margin-bottom: 25px;">
            {formatted_pronunciation}
        </div>

        <h3 style="color: #333;">English Translation</h3>
        <div style="background: #fdfaf2; border-left: 4px solid #f9a825; padding: 15px; font-size: 16px;">
            {formatted_english}
        </div>
    </div>
    """
    send_email(to_email, f"{language} Practice: Breakdown & Translation", html_content)