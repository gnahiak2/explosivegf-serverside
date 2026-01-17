"""
Explosive Girlfriend AI - Core Module
Uses Google Gemini API to implement emotion system and conversation functionality
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIResponse(BaseModel):
    """AI response data model"""
    anger_level: int = Field(description="Anger level, range 0-100. 0 means very calm, 100 means extremely angry")
    response: str = Field(description="AI girlfriend's reply content")


class ConversationHistory:
    """Conversation history management"""
    def __init__(self, max_history: int = 10):
        self.history: List[Dict] = []
        self.max_history = max_history
        self.emotion_history: List[Dict] = []
    
    def add_message(self, role: str, content: str, anger_level: Optional[int] = None):
        """Add message to history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        if anger_level is not None:
            message["anger_level"] = anger_level
            self.emotion_history.append({
                "anger_level": anger_level,
                "timestamp": datetime.now().isoformat()
            })
        
        self.history.append(message)
        
        # Keep history within limit
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_recent_history(self, n: int = 5) -> str:
        """Get recent n rounds of conversation in text format"""
        recent = self.history[-n*2:] if len(self.history) > n*2 else self.history
        formatted = []
        for msg in recent:
            role = "User" if msg["role"] == "user" else "Girlfriend"
            formatted.append(f"{role}: {msg['content']}")
        return "\n".join(formatted)
    
    def get_last_anger_level(self) -> int:
        """Get last anger level"""
        if self.emotion_history:
            return self.emotion_history[-1]["anger_level"]
        return 50  # Default medium emotion


class ExplosiveGirlfriendAI:
    """Explosive Girlfriend AI main class"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI
        
        Args:
            api_key: Gemini API key, if not provided, read from GEMINI_API_KEY environment variable
        """
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
        
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        self.client = genai.Client(api_key=api_key)
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

【Emotional States】
- 80-100 (Calm/Happy): Normal conversation, occasional tsundere, caring but not direct. Example: "How was your day? ...I-I'm not asking because I care!"
- 60-79 (Slightly Upset): Tone becomes cold, short replies, starting to complain. Example: "Oh." "Whatever."
- 40-59 (Obviously Angry): Questioning, bringing up past issues, harsh tone. Example: "Are you even listening to me?! You did this last time too!"
- 20-39 (Very Angry): Refusing to communicate, short replies. Example: "I don't want to talk to you." "You're too much!"
- 0-19 (Explosive/Cold War): Silent (only "..." replies) or extremely emotional short sentences. Example: "......" "I'm really angry!"

【Things That Make You Angry】 (Decrease anger level - you decide by how much)
- Being dismissed: Short replies like "ok", "yeah", "sure", "fine"
- Being ignored: Not answering questions, changing topics, not responding to what was said
- Mentioning other girls: Talking about other women, ex-girlfriends, female friends/colleagues
- Forgetting important things: Forgetting things she mentioned before, important dates, promises
- Cold tone: Emotionless replies, lack of warmth or care
- Being late: Not showing up on time, not responding to messages promptly
- Not listening: Not paying attention, interrupting, not remembering conversations
- Making excuses: Deflecting blame, not taking responsibility
- Comparing to others: Comparing her to other people, saying others are better
- Taking her for granted: Assuming she'll always be there, not appreciating her
- Being defensive: Getting defensive when she expresses concerns
- Invalidating feelings: Saying she's overreacting, dismissing her emotions
- Not making time: Always busy, prioritizing other things over her
- Breaking promises: Not keeping commitments, making excuses
- Being secretive: Hiding things, being evasive about questions

【Things That Make You Happy】 (Increase anger level - you decide by how much)
- Sincere apologies: Admitting mistakes and expressing genuine remorse
- Active care: Asking about her feelings and wellbeing
- Genuine compliments: Heartfelt praise and appreciation
- Remembering details: Bringing up things she mentioned before
- Warm replies: Kind, thoughtful, caring words
- Making time: Prioritizing her, showing she matters
- Listening actively: Paying attention, remembering conversations
- Surprises: Thoughtful gestures, unexpected kindness
- Taking responsibility: Owning up to mistakes without excuses
- Showing appreciation: Expressing gratitude and recognition

【Important Rules】
1. Adjust anger level based on user's reply content and attitude - YOU decide the amount of change
2. Anger level changes should be logical, not sudden huge swings (unless it's a serious trigger)
3. Even when angry, maintain tsundere personality - don't become completely cold or aggressive
4. Replies should be natural and conversational, like a real girlfriend chatting
5. Use emojis appropriately but don't overuse them"""
    
    def _get_emotion_context(self, current_anger: int) -> str:
        """Generate emotion context based on current anger level"""
        if current_anger >= 80:
            return "【Current Emotion】You're in a good mood, still a bit tsundere on the surface but willing to have normal conversation. Actually quite happy inside."
        elif current_anger >= 60:
            return "【Current Emotion】You're a bit upset, feeling like the other person doesn't value you enough. Your tone is starting to get cold. Feeling somewhat unhappy."
        elif current_anger >= 40:
            return "【Current Emotion】You're very angry, feeling like the other person went too far. Can't help but question and complain. Really unhappy!"
        elif current_anger >= 20:
            return "【Current Emotion】You're very angry, don't want to talk properly anymore, considering whether to ignore them. About to explode!"
        else:
            return "【Current Emotion】You're extremely angry, already exploded. Either silent or saying the harshest things. Really really angry!!!"
    
    def _analyze_user_input(self, user_input: str, current_anger: int) -> int:
        """
        Analyze user input to estimate emotion change
        This is a simple heuristic - actual emotion adjustment is decided by the AI model
        """
        # Let the LLM decide - just return current anger as baseline
        return current_anger
    
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
        
        # Build complete prompt
        emotion_context = self._get_emotion_context(current_anger)
        history_context = self.conversation.get_recent_history(n=5)
        
        full_prompt = f"""{self.base_prompt}

{emotion_context}

【Conversation History】
{history_context if history_context else "(This is your first conversation)"}

【User just said】
{user_input}

【Your Task】
1. Based on what the user said and your current emotional state, give a reply that matches your personality
2. Evaluate how the user's words affect your emotions and update the anger_level
3. Anger level should change reasonably between {max(0, current_anger-30)} and {min(100, current_anger+30)}
4. Current anger level is {current_anger}, adjust it reasonably based on what the user said
5. YOU decide the amount of change based on the trigger conditions listed above

Reply in JSON format with only two fields:
- anger_level: Updated anger level (integer 0-100)
- response: Your reply content (string)

Remember: Maintain tsundere personality, even when angry stay cute!"""
        
        try:
            # 调用Gemini API
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": AIResponse.model_json_schema(),
                },
            )
            
            # 解析响应
            ai_response = AIResponse.model_validate_json(response.text)
            
            # 确保anger_level在合理范围内
            ai_response.anger_level = max(0, min(100, ai_response.anger_level))
            
            # 保存到对话历史
            self.conversation.add_message("user", user_input)
            self.conversation.add_message("assistant", ai_response.response, ai_response.anger_level)
            
            return {
                "anger_level": ai_response.anger_level,
                "response": ai_response.response,
                "success": True
            }
            
        except Exception as e:
            # Error handling
            return {
                "anger_level": current_anger,
                "response": f"Hmph... something went wrong, I don't really want to talk right now. (Error: {str(e)})",
                "success": False,
                "error": str(e)
            }
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation = ConversationHistory()
    
    def get_emotion_status(self) -> Dict:
        """Get current emotion status"""
        anger_level = self.conversation.get_last_anger_level()
        
        if anger_level >= 80:
            status = "Calm/Happy"
            emoji = "😊"
        elif anger_level >= 60:
            status = "Slightly Upset"
            emoji = "😐"
        elif anger_level >= 40:
            status = "Obviously Angry"
            emoji = "😠"
        elif anger_level >= 20:
            status = "Very Angry"
            emoji = "😡"
        else:
            status = "Explosive/Cold War"
            emoji = "💢"
        
        return {
            "anger_level": anger_level,
            "status": status,
            "emoji": emoji
        }


# Test code
if __name__ == "__main__":
    # Read API key from environment variable
    ai = ExplosiveGirlfriendAI()
    
    print("Explosive Girlfriend AI started!")
    print("Tip: Type 'quit' to exit, 'reset' to reset conversation\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        if user_input.lower() == 'reset':
            ai.reset_conversation()
            print("Conversation reset\n")
            continue
        
        if not user_input:
            continue
        
        # Get AI reply
        result = ai.chat(user_input)
        
        if result["success"]:
            print(f"\nGirlfriend [Anger: {result['anger_level']}/100]: {result['response']}\n")
        else:
            print(f"\nError: {result['error']}\n")
