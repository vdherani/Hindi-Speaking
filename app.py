import uuid
import threading
from flask import Flask, request
from ai_text_generator import get_daily_lesson
from email_sender import send_initial_email, send_translation_email

app = Flask(__name__)

# This dictionary stores your translations temporarily while the timer runs
active_sessions = {}

def delayed_translation_email(session_id):
    """This function runs in the background after the 20-minute delay."""
    session_data = active_sessions.get(session_id)
    if session_data:
        send_translation_email(
            roman_hindi=session_data["roman"],
            english_translation=session_data["english"]
        )
        # Clean up the memory after sending
        del active_sessions[session_id]

@app.route("/send-daily")
def trigger_daily_email():
    """Route to generate and send the morning email."""
    # 1. Get the AI text
    lesson = get_daily_lesson()
    
    # 2. Create a unique ID for today's lesson
    session_id = str(uuid.uuid4())
    
    # 3. Store the translations in memory for later
    active_sessions[session_id] = {
        "roman": lesson["roman_hindi"],
        "english": lesson["english_translation"]
    }
    
    # 4. Send Email #1
    # request.host_url ensures the email link points to your live server automatically
    base_url = request.host_url.rstrip('/')
    send_initial_email(lesson["hindi_text"], session_id, base_url)
    
    return "Daily email successfully triggered and sent!"

@app.route("/start-timer")
def start_timer():
    """Route that triggers when you click the email button."""
    session_id = request.args.get("session_id")
    
    if not session_id or session_id not in active_sessions:
        return "Invalid or expired session. Have you already requested this translation?"

    # Set the delay to 20 minutes (20 minutes * 60 seconds)
    # NOTE: Change this to 10 for testing so you don't have to wait 20 minutes!
    delay_in_seconds = 20  
    
    # Start the background timer
    timer = threading.Timer(delay_in_seconds, delayed_translation_email, args=[session_id])
    timer.start()
    
    return """
    <h1 style="color: #1a73e8; font-family: sans-serif; text-align: center; margin-top: 50px;">
        ⏳ Timer Started!
    </h1>
    <p style="font-family: sans-serif; text-align: center; font-size: 18px;">
        Your 20 minutes have begun. The translation will arrive in your inbox shortly.
    </p>
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)