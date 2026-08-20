import os
import json
import random
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class HindiLesson(BaseModel):
    hindi_text: str
    roman_hindi: str
    english_translation: str

def get_daily_lesson():
    """Fetches a daily 5-minute Hindi reading exercise."""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    
    # 1. Create a list of varied topics and formats
    scenarios = [
        "A fascinating short story from Indian folklore or mythology.",
        "A realistic, slightly dramatic dialogue between two friends arguing about travel plans.",
        "A detailed first-person journal entry about a chaotic but fun wedding.",
        "An interesting cultural explanation of how a specific Indian street food is made.",
        "A comedic story about a misunderstanding at a workplace.",
        "A thoughtful opinion piece on the balance between modern life and tradition."
    ]
    
    # 2. Pick a random scenario each day
    daily_topic = random.choice(scenarios)
    
    # 3. Inject it into a highly specific prompt
    prompt = f"""
    Write a comprehensive and engaging Hindi text based on this topic: {daily_topic}
    
    Strict Requirements:
    * Length: The text must be roughly 250 to 350 words long. 
    * Structure: Use multiple paragraphs. Mix short, punchy sentences with longer, complex ones.
    * Target Audience: An intermediate Hindi learner. Use natural, conversational grammar but avoid overly obscure vocabulary.
    """
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=HindiLesson,
            temperature=0.8, # Slightly higher temperature for better creative storytelling
        ),
    )
    
    return json.loads(response.text)

if __name__ == "__main__":
    lesson = get_daily_lesson()
    print(f"Hindi Text ({len(lesson['hindi_text'].split())} words):\n{lesson['hindi_text']}\n")
    print("Roman Hindi preview:", lesson["roman_hindi"][:100], "...")