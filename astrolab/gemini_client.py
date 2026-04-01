import os
import json
import random
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class GeminiClient:
    """Client for Google Gemini API with smart fallback for demonstrations."""
    
    def __init__(self):
        # Uses gemini-2.5-flash for quick text tasks
        if GEMINI_API_KEY:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
            
        self._load_demo_cache()

    def _load_demo_cache(self):
        """Loads cached data for offline demonstration."""
        cache_path = os.path.join(os.path.dirname(__file__), "demo_cache.json")
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                self.demo_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.demo_data = {"quizzes": [], "deep_dives": [], "flashcards": {}}

    def _generate_json(self, prompt: str) -> dict:
        """Helper to ensure the response is valid JSON."""
        if not self.model:
            raise ValueError("GEMINI_API_KEY not configured.")
            
        full_prompt = f"{prompt}\n\nRespond ONLY with a valid JSON object, without markdown formatting or extra text."
        
        response = self.model.generate_content(full_prompt)
        text = response.text.strip()
        
        # Removes possible markdown code blocks returned by the model
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Fallback in case of generation error
            return {"error": "Failed to decode JSON from Gemini", "raw_text": text}

    def generate_quiz(self, context_text: str, num_questions: int = 5) -> list:
        """Generates a quiz based on the provided text."""
        if not self.model:
            return self._fallback_quiz()

        prompt = f"""
        Based on the following astronomy text, create a quiz with {num_questions} multiple-choice questions.
        The level should be for university students (challenging but focused on the text's concepts).
        
        TEXT:
        {context_text}
        
        The output JSON must strictly be a list of objects with this format:
        [
            {{
                "question": "question text",
                "options": ["A) op1", "B) op2", "C) op3", "D) op4"],
                "answer": "A) op1",  // MUST match exactly one of the strings in the options list
                "explanation": "Why this is the correct answer based on the text"
            }}
        ]
        """
        try:
            result = self._generate_json(prompt)
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "quiz" in result: # Handles slight structural variations
                return result["quiz"]
            return self._fallback_quiz()
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return self._fallback_quiz()

    def generate_flashcard(self, topic: str, context_text: str) -> dict:
        """Generates flashcard content."""
        if not self.model:
            return self._fallback_flashcard(topic)

        prompt = f"""
        Based on the NASA text about '{topic}', create the content for a study flashcard.
        
        TEXT:
        {context_text}
        
        The output JSON must be an object with this format:
        {{
            "front": "A direct question or key concept about {topic}",
            "back": "The detailed, direct, and easy-to-memorize answer"
        }}
        """
        try:
            result = self._generate_json(prompt)
            if "front" in result and "back" in result:
                return result
            return self._fallback_flashcard(topic)
        except Exception:
            return self._fallback_flashcard(topic)

    def generate_deep_dive(self, wrong_answers: list) -> str:
        """Generates an in-depth explanation based on errors."""
        if not self.model:
            return self.demo_data.get("deep_dives", ["Sorry, offline mode. Check the documentation to enable AI."])[0]
            
        formatted_errors = ""
        for i, q in enumerate(wrong_answers, 1):
            formatted_errors += f"Error {i}:\n"
            formatted_errors += f"Question: {q.get('question')}\n"
            formatted_errors += f"Correct Answer: {q.get('answer')}\n\n"

        prompt = f"""
        You are a university astrophysics professor passionate about teaching. 
        A student just took an astronomy quiz and missed the following questions:

        {formatted_errors}

        Please create a short, in-depth study guide (Deep Dive) focused ONLY on these concepts.
        Your response does not need to be JSON. Use Markdown freely.
        - Explain the physical intuition behind each error.
        - Use everyday analogies to aid memorization.
        - Be encouraging.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"An error occurred generating the Deep Dive: {e}"

    def _fallback_quiz(self) -> list:
        """Returns a rich fixed quiz from cache if the API fails."""
        quizzes = self.demo_data.get("quizzes", [])
        if quizzes:
            return random.choice(quizzes)
        return []
        
    def _fallback_flashcard(self, topic: str) -> dict:
        """Returns a flashcard from the demo cache."""
        cards = self.demo_data.get("flashcards", {})
        # Tries to find a card matching the topic, otherwise gets default
        topic_lower = topic.lower()
        if topic_lower in cards:
            return cards[topic_lower]
        return cards.get("default", {"front": "Offline Mode", "back": "Add GEMINI_API_KEY to .env"})

gemini_client = GeminiClient()
