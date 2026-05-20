from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import uuid

from database import get_db
from schemas import ChatRequest, ChatResponse, ChatHistory
from services.gemini_service import get_ai_response

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Send a message to the AI chatbot.
    Supports multi-turn conversations via session_id.
    """
    db = get_db()

    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    # Load existing chat history
    session = await db.chat_sessions.find_one({"session_id": session_id})
    history = session.get("messages", []) if session else []

    # Add current user message to history
    user_msg = {
        "role": "user",
        "content": request.message,
        "timestamp": now.isoformat()
    }
    history.append(user_msg)

    # Get Gemini response
    ai_result = await get_ai_response(
        user_message=request.message,
        chat_history=history,
        user_name=request.user_name
    )

    assistant_msg = {
        "role": "model",
        "content": ai_result["reply"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    history.append(assistant_msg)

    # Save/update chat session in MongoDB
    if session:
        await db.chat_sessions.update_one(
            {"session_id": session_id},
            {"$set": {"messages": history, "updated_at": now}}
        )
    else:
        await db.chat_sessions.insert_one({
            "session_id": session_id,
            "user_name": request.user_name,
            "messages": history,
            "created_at": now,
            "updated_at": now
        })

    # Log automation event
    await db.automation_logs.insert_one({
        "workflow": "chatbot_interaction",
        "trigger": "user_message",
        "status": "success" if ai_result["success"] else "error",
        "details": {
            "session_id": session_id,
            "message_preview": request.message[:100]
        },
        "created_at": now
    })

    return ChatResponse(
        session_id=session_id,
        reply=ai_result["reply"],
        timestamp=now,
        tokens_used=ai_result.get("tokens_used")
    )


@router.get("/history/{session_id}", response_model=ChatHistory)
async def get_chat_history(session_id: str):
    """Get full conversation history for a session."""
    db = get_db()
    session = await db.chat_sessions.find_one({"session_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return ChatHistory(
        session_id=session_id,
        messages=session.get("messages", []),
        created_at=session["created_at"],
        updated_at=session["updated_at"]
    )


@router.delete("/history/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear/reset a chat session."""
    db = get_db()
    result = await db.chat_sessions.delete_one({"session_id": session_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session cleared", "session_id": session_id}


@router.get("/sessions")
async def list_sessions(limit: int = 20, skip: int = 0):
    """List all chat sessions (admin view)."""
    db = get_db()
    cursor = db.chat_sessions.find(
        {},
        {"session_id": 1, "user_name": 1, "created_at": 1, "updated_at": 1, "messages": {"$slice": -1}}
    ).sort("updated_at", -1).skip(skip).limit(limit)

    sessions = []
    async for s in cursor:
        s["_id"] = str(s["_id"])
        sessions.append(s)

    total = await db.chat_sessions.count_documents({})
    return {"sessions": sessions, "total": total, "skip": skip, "limit": limit}
