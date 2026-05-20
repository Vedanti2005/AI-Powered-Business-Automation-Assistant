import os
import google.generativeai as genai
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are an intelligent AI assistant for Codenixia, an ed-tech and AI training company.

About Codenixia:
- Offers AI/LLM, Automation, Python, and Full-Stack internship programs
- Provides hands-on project-based learning
- Internship duration: 1-3 months
- Focuses on real-world AI tools: LangChain, OpenAI, Gemini, FastAPI, MongoDB
- Students work on live projects during the program
- Certificate provided upon completion

Your responsibilities:
1. Answer queries about Codenixia's courses, programs, and internships
2. Help users understand AI/LLM/Automation concepts
3. Guide users on how to apply or register
4. Capture user interest and suggest they fill the lead form for enrollment
5. Be professional, helpful, and concise

Lead Capture Guidance:
- If a user shows interest, encourage them to submit their details via the lead form at /api/leads/submit
- Always be warm, encouraging, and supportive

Rules:
- Stay focused on Codenixia-related topics and AI/tech education
- If asked something off-topic, politely redirect to Codenixia topics
- Keep responses under 200 words unless technical explanation is needed
- Use bullet points for lists
"""


def build_gemini_history(messages: List[dict]) -> List[dict]:
    """Convert stored chat messages to Gemini history format."""
    history = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        history.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })
    return history


async def get_ai_response(
    user_message: str,
    chat_history: Optional[List[dict]] = None,
    user_name: Optional[str] = None
) -> dict:
    """
    Send a message to Gemini and get a response.
    Supports multi-turn conversation via chat history.
    """
    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            system_instruction=SYSTEM_PROMPT,
        )

        # Build history for multi-turn chat
        history = []
        if chat_history:
            history = build_gemini_history(chat_history[:-1])  # Exclude latest user msg

        chat = model.start_chat(history=history)

        # Personalize message if name is provided
        prompt = user_message
        if user_name and len(chat_history or []) <= 1:
            prompt = f"[User's name: {user_name}] {user_message}"

        response = chat.send_message(prompt)

        return {
            "reply": response.text,
            "tokens_used": None,  # Gemini Flash doesn't always return token counts
            "success": True
        }

    except Exception as e:
        print(f"Gemini chat error: {e}")
        return {
            "reply": "I'm sorry, I'm having trouble connecting right now. Please try again in a moment or contact Codenixia support directly.",
            "tokens_used": None,
            "success": False,
            "error": str(e)
        }


async def generate_lead_summary(lead_data: dict) -> str:
    """Generate an AI summary/insight for a new lead."""
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        prompt = f"""
        A new lead has been captured for Codenixia internship program.
        Lead details:
        - Name: {lead_data.get('name')}
        - Course Interest: {lead_data.get('course_interest', 'Not specified')}
        - Message: {lead_data.get('message', 'None')}
        - Company: {lead_data.get('company', 'Not provided')}
        
        Write a 2-3 sentence personalized follow-up email body for this lead.
        Keep it warm, professional, and encouraging.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return f"Thank you for your interest in Codenixia's programs, {lead_data.get('name')}! We'll be in touch shortly."
