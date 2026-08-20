import os
import random
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Define the structured output format
class LanguageLesson(BaseModel):
    target_language_text: str
    pronunciation_guide: str  # Romanized/phonetic breakdown (or pronunciation tips for Latin scripts)
    english_translation: str

SCENARIOS = [
    "Ordering at a local cafe or street market",
    "Asking a friendly local for directions to a landmark",
    "Discussing daily morning routines and hobbies",
    "Buying tickets at a train or bus station",
    "A casual conversation about the weekend weather",
    "Checking in at a hotel and asking about breakfast",
    "Meeting a neighbor and introducing yourself"
]

def get_daily_lesson(language: str = "Hindi", level: str = "Beginner") -> dict:
    """Generates a dynamic reading lesson tailored to the user's language and level."""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    scenario = random.choice(SCENARIOS)

    prompt = f"""
    You are an expert language teacher. Create a short daily reading lesson for a {level} student learning {language}.

    Topic / Scenario: {scenario}

    Requirements:
    1. 'target_language_text': A short natural conversation or paragraph in {language} (3 to 6 sentences). Use authentic native script (e.g., Devanagari for Hindi, Kanji/Kana for Japanese, Cyrillic for Russian, etc.).
    2. 'pronunciation_guide': Provide a clear phonetic/romanized transliteration for languages with non-Latin scripts (e.g., Pinyin, Romaji, Roman Hindi). If the language uses the Latin alphabet (e.g., Spanish, French, German), provide syllable stress or key pronunciation notes for tricky words.
    3. 'english_translation': A natural English translation of the entire passage.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": LanguageLesson,
        },
    )

    lesson_data = LanguageLesson.model_validate_json(response.text)
    return lesson_data.model_dump()

if __name__ == "__main__":
    test_lesson = get_daily_lesson("Hindi", "Beginner")
    print(test_lesson)
