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
    # Mystery & Discovery
    "A person finds an old, dusty key inside a vintage book bought at a flea market.",
    "A strange, glowing door appears at the back of a routine grocery store aisle.",
    "A detective questions an unusually calm cat who seems to have witnessed a missing jewelry case.",
    "A traveler discovers an uncharted coffee shop that only appears during rainy afternoons.",

    # Comedy & Mishaps
    "A chef accidentally invents a dish that makes everyone who eats it uncontrollably honest.",
    "A time traveler tries to order modern fast food without revealing they are from the year 1850.",
    "Two neighbors both try to secretly return a runaway pet parrot who only repeats gossip.",
    "A student attempts to bake a birthday cake using an ancient recipe and ends up with a chaotic kitchen.",

    # Adventure & Cozy Life
    "A quiet night at a train cabin heading through snowy mountains while sharing tea with a stranger.",
    "A street musician plays a melody that makes all nearby stray dogs gather and sit in a polite circle.",
    "A photographer spots a rare, legendary bird sitting calmly on their balcony railing.",
    "A botanist discovers a peculiar flower in their greenhouse that gently hums when watered.",
]

def get_daily_lesson(language: str = "Hindi", level: str = "Beginner") -> dict:
    """Generates a dynamic reading lesson tailored to the user's language and level."""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    scenario = random.choice(SCENARIOS)

    prompt = f"""
    You are an engaging storyteller and language teacher. 
    Write an entertaining, creative short story (less than 500 words) for a {level} learner studying {language}.

    Story Premise: {scenario}

    Requirements:
    1. 'target_language_text': A fun, narrative short story in {language}. Keep the vocabulary and grammar natural and appropriate for a {level} level. Use authentic native script (e.g., Devanagari for Hindi, Kanji/Kana for Japanese, Cyrillic for Russian, etc.).
    2. 'pronunciation_guide': Provide a clear phonetic/romanized transliteration for non-Latin scripts (e.g., Roman Hindi, Romaji, Pinyin). For Latin scripts (Spanish, French, etc.), provide pronunciation/intonation tips for key phrases.
    3. 'english_translation': A smooth, natural English translation of the story.
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
