"""
Explosive Girlfriend AI - Core Module
Facial expression is CONTEXT ONLY (no backend emotion math)
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime

import google.generativeai as genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# -------------------- Models --------------------

class AIResponse(BaseModel):
    anger_level: int = Field(ge=0, le=120)
    response: str


# -------------------- Helpers --------------------

def parse_ai_response(raw_text: str) -> dict:
    """
    Gemini may return:
    - JSON object
    - JSON list with one object
    Normalize it.
    """
    data = json.loads(raw_text)

    if isinstance(data, list):
        if not data:
            raise ValueError("Empty list returned from model")
        return data[0]

    if isinstance(data, dict):
        return data

    raise ValueError("Invalid JSON format from model")


# -------------------- Conversation --------------------

class ConversationHistory:
    def __init__(self, max_history: int = 10):
        self.history: List[Dict] = []
        self.emotion_history: List[Dict] = []
        self.max_history = max_history

    def add_message(self, role: str, content: str, anger_level: Optional[int] = None):
        msg = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

        if anger_level is not None:
            msg["anger_level"] = anger_level
            self.emotion_history.append({
                "anger_level": anger_level,
                "timestamp": datetime.now().isoformat()
            })

        self.history.append(msg)

        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_recent_history(self, n: int = 5) -> str:
        recent = self.history[-n * 2:] if len(self.history) > n * 2 else self.history
        return "\n".join(
            f"{'User' if m['role']=='user' else 'Girlfriend'}: {m['content']}"
            for m in recent
        )

    def get_last_anger_level(self) -> int:
        if self.emotion_history:
            return self.emotion_history[-1]["anger_level"]
        return 75  # default starting anger


# -------------------- AI Core --------------------

class ExplosiveGirlfriendAI:
    def __init__(self, api_key: Optional[str] = None):
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")

        genai.configure(api_key=api_key)

        self.conversation = ConversationHistory()
        self.base_prompt = self._create_base_prompt()

    def _create_base_prompt(self) -> str:
        return """
You are a tsundere girlfriend AI.

Personality:
- Easily annoyed, emotional, dramatic
- Tsundere: harsh words, hidden care
- Jealous and reactive

Rules:
- Always consider the user's FACIAL EXPRESSION when interpreting intent
- Facial expression affects HOW you read the message, not WHAT they say
- Anger scale: 0–120
- At 100+, you completely lose control and use ALL CAPS

IMPORTANT:
- Return ONE JSON OBJECT ONLY
- Do NOT wrap the response in a list
"""

    def _get_emotion_context(self, anger: int) -> str:
        if anger >= 100:
            return "Current emotion: TOTAL RAGE. SCREAM."
        elif anger >= 80:
            return "Current emotion: Extremely angry."
        elif anger >= 60:
            return "Current emotion: Very angry."
        elif anger >= 40:
            return "Current emotion: Angry."
        elif anger >= 20:
            return "Current emotion: Slightly upset."
        return "Current emotion: Calm (tsundere)."

    def chat(self, user_input: str, user_expression: str = "neutral") -> Dict:
        current_anger = self.conversation.get_last_anger_level()

        emotion_context = self._get_emotion_context(current_anger)
        history_context = self.conversation.get_recent_history()

        expression_context = f"""
【User Facial Expression】
The user's facial expression while speaking is: {user_expression.upper()}.
Interpret emotional intent using this expression.
"""

        full_prompt = f"""
{self.base_prompt}

{emotion_context}

{expression_context}

【Conversation History】
{history_context if history_context else "(First message)"}

【User just said】
{user_input}

Reply ONLY in JSON:
{{
  "anger_level": number (0–120),
  "response": string
}}
"""

        try:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json"
                )
            )

            parsed = parse_ai_response(response.text)
            ai_response = AIResponse.model_validate(parsed)

            self.conversation.add_message("user", user_input)
            self.conversation.add_message(
                "assistant",
                ai_response.response,
                ai_response.anger_level
            )

            return {
                "success": True,
                "anger_level": ai_response.anger_level,
                "response": ai_response.response
            }

        except Exception as e:
            return {
                "success": False,
                "anger_level": current_anger,
                "response": "Hmph... something broke.",
                "error": str(e)
            }

    def reset_conversation(self):
        self.conversation = ConversationHistory()

    def get_emotion_status(self) -> Dict:
        return {
            "anger_level": self.conversation.get_last_anger_level()
        }
