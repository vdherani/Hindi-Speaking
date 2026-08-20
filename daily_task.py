import json
import time
import os
from ai_generator import get_daily_lesson
from email_sender import send_initial_email, send_translation_email

# Read the JSON string directly from the GitHub Secret
users_json_string = os.getenv("USERS_JSON")

if not users_json_string:
    print("Error: USERS_JSON secret is missing or empty!")
    exit(1)

# Convert the string back into a Python list
users = json.loads(users_json_string)

# Step 1: Generate lessons and send Email #1 to all users
pending_translations = []

print(f"Processing lessons for {len(users)} user(s)...")
for user in users:
    name = user["name"]
    email = user["email"]
    language = user.get("language", "Hindi")
    level = user.get("level", "Beginner")

    print(f"Generating {language} ({level}) lesson for {name} ({email})...")
    lesson = get_daily_lesson(language=language, level=level)

    print(f"Sending initial email to {name}...")
    send_initial_email(
        to_email=email,
        user_name=name,
        language=language,
        text=lesson["target_language_text"]
    )

    # Store translation data to send in Step 2
    pending_translations.append({
        "to_email": email,
        "user_name": name,
        "language": language,
        "pronunciation": lesson["pronunciation_guide"],
        "english": lesson["english_translation"]
    })

# Step 2: Wait 20 minutes (1200 seconds)
# NOTE: You can change 20 * 60 to 10 for a quick test run!
delay_seconds = 20 
print(f"All reading emails sent. Waiting {delay_seconds // 60} minutes before dispatching translations...")
time.sleep(delay_seconds)

# Step 3: Send Email #2 to all users
print("Sending translations...")
for item in pending_translations:
    print(f"Sending translation email to {item['user_name']} ({item['to_email']})...")
    send_translation_email(
        to_email=item["to_email"],
        user_name=item["user_name"],
        language=item["language"],
        pronunciation=item["pronunciation"],
        english_translation=item["english"]
    )

print("All daily tasks completed successfully!")