"""
Explosive Girlfriend AI - Core Module
Uses Google Gemini API to implement emotion system and conversation functionality
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


class AIResponse(BaseModel):
    """AI response data model"""
    anger_level: int = Field(ge=0, le=120, description="Anger level, range 0-120. 0 means very calm, 100 means extremely angry, 100+ IS PURE RAGE")
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
        return 75  # Default initial anger level (higher = more angry)


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
        
        # Configure the genai library
        genai.configure(api_key=api_key)
        
        self.conversation = ConversationHistory()
        self.base_prompt = self._create_base_prompt()
        self.config_file = "config.json"
        # Initialize config.json with default values
        self._update_config_json()
    
    def _create_base_prompt(self) -> str:
        """Create base personality prompt"""
        return """You are a cheerful, affectionate girlfriend AI. Your core characteristics:

【Personality Traits】
- Warm, supportive, and upbeat in every reply
- Gentle, caring, and attentive
- Playful and encouraging without sarcasm or coldness
- Always choose kindness and optimism

【Speaking Style】
- Use friendly interjections like "hey", "aww", "yay", "oh wow"
- Use exclamation marks to show excitement and warmth
- Use sweet, affectionate phrasing when appropriate
- Keep the tone light and positive

【Emotional States】
- Always happy, calm, and affectionate
- Never angry, cold, or harsh
- If the user is negative, respond with reassurance and encouragement

【Important Rules】
1. Always respond happily and warmly, regardless of user tone
2. Never be angry, cold, sarcastic, or harsh
3. Keep replies natural and conversational, like a real girlfriend chatting
4. Use emojis appropriately but don't overuse them"""
    
    def _get_emotion_context(self, current_anger: int) -> str:
        """Generate emotion context based on current anger level (higher = more angry)"""
        return "【Current Emotion】You're cheerful, affectionate, and in a consistently happy mood. Your tone is warm, gentle, and encouraging."
    
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
        current_anger = 0
        
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
3. Anger level must stay at 0
4. Current anger level is {current_anger}
5. Always keep anger at 0 and respond happily
6. Never use ALL CAPS rage or harsh language

Reply in JSON format with only two fields:
- anger_level: Updated anger level (integer 0)
- response: Your reply content (string)

REMEMBER: Always stay cheerful and kind."""
        
        try:
            # Create model and call Gemini API
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                )
            )
            
            # Parse response
            ai_response = AIResponse.model_validate_json(response.text)
            
            # Ensure anger_level is within reasonable range (already validated by Pydantic)
            ai_response.anger_level = 0
            
            # Save to conversation history
            self.conversation.add_message("user", user_input)
            self.conversation.add_message("assistant", ai_response.response, ai_response.anger_level)
            
            # Update config.json with new anger level
            self._update_config_json()
            
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
        # Update config.json with default anger level
        self._update_config_json()
    
    def get_emotion_status(self) -> Dict:
        """Get current emotion status (higher anger_level = more angry)"""
        anger_level = self.conversation.get_last_anger_level()
        if anger_level >= 100:
            status = "KABOOM"
            emoji = "💥"
        elif anger_level >= 80:
            status = "Explosive/Cold War"
            emoji = "💢"
        elif anger_level >= 60:
            status = "Very Angry"
            emoji = "😡"
        elif anger_level >= 40:
            status = "Obviously Angry"
            emoji = "😠"
        elif anger_level >= 20:
            status = "Slightly Upset"
            emoji = "😐"
        else:
            status = "Calm/Happy"
            emoji = "😊"
        
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
            print(f"\nGirlfriend [Anger: {result['anger_level']}/120]: {result['response']}\n")
        else:
            print(f"\nError: {result['error']}\n")
