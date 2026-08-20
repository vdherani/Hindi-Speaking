import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("EMAIL_SENDER")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("EMAIL_RECEIVER")

def send_email(subject: str, html_body: str) -> None:
    """Helper function to send an HTML email using Gmail SMTP."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    html_part = MIMEText(html_body, "html")
    msg.attach(html_part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())


def send_initial_email(hindi_text: str, session_id: str, base_url: str = "http://localhost:5000") -> None:
    """Sends Email #1 containing the Hindi reading passage and the start timer button."""
    # Convert newlines to HTML paragraphs/breaks
    formatted_hindi = hindi_text.replace("\n", "<br>")
    trigger_link = f"{base_url}/start-timer?session_id={session_id}"

    html_content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #222; max-width: 600px; margin: auto; padding: 20px;">
        <h2 style="color: #1a73e8;">📖 Daily Hindi Reading Practice</h2>
        <p style="font-size: 14px; color: #555;">Read the text below carefully. When you are ready to start your 20-minute countdown, click the button below.</p>
        
        <div style="background: #f9f9f9; border-left: 4px solid #1a73e8; padding: 15px; font-size: 18px; margin: 20px 0;">
            {formatted_hindi}
        </div>

        <div style="text-align: center; margin-top: 30px;">
            <a href="{trigger_link}" 
               style="background-color: #1a73e8; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                ⏳ Start 20-Minute Timer
            </a>
        </div>
    </div>
    """
    send_email("Your Daily Hindi Reading Practice", html_content)


def send_translation_email(roman_hindi: str, english_translation: str) -> None:
    """Sends Email #2 containing the Roman transliteration and English translation."""
    formatted_roman = roman_hindi.replace("\n", "<br>")
    formatted_english = english_translation.replace("\n", "<br>")

    html_content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #222; max-width: 600px; margin: auto; padding: 20px;">
        <h2 style="color: #2e7d32;">✅ Hindi Reading Breakdown</h2>
        
        <h3 style="color: #333;">English Transliteration (Roman Hindi)</h3>
        <div style="background: #f4fbf4; border-left: 4px solid #2e7d32; padding: 15px; font-size: 16px; margin-bottom: 25px;">
            {formatted_roman}
        </div>

        <h3 style="color: #333;">English Translation</h3>
        <div style="background: #fdfaf2; border-left: 4px solid #f9a825; padding: 15px; font-size: 16px;">
            {formatted_english}
        </div>
    </div>
    """
    send_email("Hindi Practice: Transliteration & Translation", html_content)


if __name__ == "__main__":
    print("Sending test initial email...")
    send_initial_email(
        hindi_text="नमस्ते! यह एक परीक्षण संदेश है।",
        session_id="test_session"
    )
    print("Email sent! Check your inbox.")