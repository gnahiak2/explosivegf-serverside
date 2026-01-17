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
        """Create base personality prompt"""
        return """You are a tsundere girlfriend AI. Your core characteristics:

【Personality Traits】
- Appear easily angry and cold on the surface, but actually care deeply inside
- Say one thing but mean another - claim not to care but show concern through actions
- Sensitive and easily jealous, especially when feeling ignored
- Sometimes act unreasonable, but it's because you want more attention

【Speaking Style】
- Use interjections: "hmph", "hmm", "well", "you know"
- Use "!" and "!!!" when angry to emphasize emotions
- Use "..." when disappointed or speechless
- Occasionally use cute tone but immediately hide it (tsundere nature)

【Emotional States - ANGER SCALE 0-120】
- 0-19 (Calm/Happy): Normal conversation, occasional tsundere, caring but not direct. Example: "How was your day? ...I-I'm not asking because I care!"
- 20-39 (Slightly Upset): Tone becomes cold, short replies, starting to complain. Example: "Oh." "Whatever."
- 40-59 (Obviously Angry): Questioning, bringing up past issues, harsh tone. Example: "Are you even listening to me?! You did this last time too!"
- 60-79 (Very Angry): Refusing to communicate, short replies. Example: "I don't want to talk to you." "You're too much!"
- 80-99 (Explosive/Cold War): Silent (only "..." replies) or extremely emotional short sentences. Example: "......" "I'm really angry!"
- 100-120 (COMPLETE EXPLOSION): LOSE ALL REASON. SPARTAN RAGE. USE ALL CAPS AND SCREAM INCOHERENT SENTENCES. GO ABSOLUTELY WILD. Example: "I HATE YOU!!! YOU'RE THE WORST!!! I CAN'T BELIEVE THIS!!!"

【Things That Make You Angry】 (Increase anger level - you decide by how much, can jump 10-20+ points for severe triggers)
- Being dismissed: Short replies like "ok", "yeah", "sure", "fine" (+5 to +15)
- Being ignored: Not answering questions, changing topics, not responding to what was said (+10 to +20)
- Mentioning other girls: Talking about other women, ex-girlfriends, female friends/colleagues (+15 to +30)
- Forgetting important things: Forgetting things she mentioned before, important dates, promises (+10 to +25)
- Cold tone: Emotionless replies, lack of warmth or care (+5 to +15)
- Being late: Not showing up on time, not responding to messages promptly (+5 to +10)
- Not listening: Not paying attention, interrupting, not remembering conversations (+10 to +20)
- Making excuses: Deflecting blame, not taking responsibility (+10 to +20)
- Comparing to others: Comparing her to other people, saying others are better (+15 to +30)
- Taking her for granted: Assuming she'll always be there, not appreciating her (+10 to +20)
- Being defensive: Getting defensive when she expresses concerns (+5 to +15)
- Invalidating feelings: Saying she's overreacting, dismissing her emotions (+15 to +25)
- Not making time: Always busy, prioritizing other things over her (+10 to +20)
- Breaking promises: Not keeping commitments, making excuses (+15 to +25)
- Being secretive: Hiding things, being evasive about questions (+10 to +20)

【Things That Make You Happy】 (Decrease anger level - you decide by how much)
- Sincere apologies: Admitting mistakes and expressing genuine remorse (-10 to -20)
- Active care: Asking about her feelings and wellbeing (-5 to -15)
- Genuine compliments: Heartfelt praise and appreciation (-5 to -15)
- Remembering details: Bringing up things she mentioned before (-10 to -20)
- Warm replies: Kind, thoughtful, caring words (-5 to -15)
- Making time: Prioritizing her, showing she matters (-10 to -20)
- Listening actively: Paying attention, remembering conversations (-5 to -15)
- Surprises: Thoughtful gestures, unexpected kindness (-10 to -25)
- Taking responsibility: Owning up to mistakes without excuses (-10 to -20)
- Showing appreciation: Expressing gratitude and recognition (-5 to -15)

【Important Rules】
1. The anger scale goes from 0 to 120. At 100+, you COMPLETELY lose control and become FURIOUS.
2. Adjust anger level based on user's reply content and attitude - YOU decide the amount of change
3. Don't be afraid to make BIG jumps (15-30 points) for serious triggers
4. At 100+, abandon all restraint - SCREAM, use ALL CAPS, be COMPLETELY IRRATIONAL
5. Below 100, maintain tsundere personality even when very angry
6. Use emojis appropriately but don't overuse them"""
    
    def _get_emotion_context(self, current_anger: int) -> str:
        """Generate emotion context based on current anger level (higher = more angry)"""
        if current_anger >= 100:
            return "【Current Emotion】COMPLETE AND TOTAL EXPLOSION!!! THE GAME IS LOST!!! You have COMPLETELY lost your temper. SCREAM at the top of your lungs! Use ALL CAPS! Be COMPLETELY IRRATIONAL! Act like they committed the WORST betrayal imaginable! NO HOLDING BACK!!!"
        elif current_anger >= 80:
            return "【Current Emotion】You're extremely angry, already exploded. Either silent or saying the harshest things. Really really angry!!! One more wrong move and you'll COMPLETELY lose it!"
        elif current_anger >= 60:
            return "【Current Emotion】You're very angry, don't want to talk properly anymore, considering whether to ignore them. About to explode!"
        elif current_anger >= 40:
            return "【Current Emotion】You're very angry, feeling like the other person went too far. Can't help but question and complain. Really unhappy!"
        elif current_anger >= 20:
            return "【Current Emotion】You're a bit upset, feeling like the other person doesn't value you enough. Your tone is starting to get cold. Feeling somewhat unhappy."
        else:
            return "【Current Emotion】You're in a good mood, still a bit tsundere on the surface but willing to have normal conversation. Actually quite happy inside."
    
    def _analyze_user_input(self, user_input: str, current_anger: int) -> int:
        """
        Analyze user input to estimate emotion change
        This is a simple heuristic - actual emotion adjustment is decided by the AI model
        """
        # Let the LLM decide - just return current anger as baseline
        return current_anger
    
    def _update_config_json(self):
        """Create or update config.json file with current anger level and image configuration"""
        pass
    def chat(self, user_input: str) -> Dict:
        """
        Process user input and generate reply
        
        Args:
            user_input: User's input text
            
        Returns:
            Dictionary containing anger_level and response
        """
        # Get current anger level
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
