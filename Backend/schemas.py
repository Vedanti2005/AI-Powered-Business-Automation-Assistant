from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ─── Enums ────────────────────────────────────────────────────────────────────

class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    REJECTED = "rejected"


class LeadSource(str, Enum):
    WEBSITE = "website"
    CHATBOT = "chatbot"
    FORM = "form"
    REFERRAL = "referral"


# ─── Lead Schemas ─────────────────────────────────────────────────────────────

class LeadCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Rahul Sharma")
    email: EmailStr = Field(..., example="rahul@example.com")
    phone: Optional[str] = Field(None, example="+91-9876543210")
    company: Optional[str] = Field(None, example="Tech Startup")
    message: Optional[str] = Field(None, example="Interested in AI internship program")
    source: LeadSource = Field(default=LeadSource.FORM)
    course_interest: Optional[str] = Field(None, example="AI/LLM Automation")

    class Config:
        use_enum_values = True


class LeadUpdate(BaseModel):
    status: Optional[LeadStatus] = None
    notes: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None

    class Config:
        use_enum_values = True


class LeadResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str]
    company: Optional[str]
    message: Optional[str]
    source: str
    status: str
    course_interest: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]


# ─── Chat Schemas ─────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str  # "user" or "model"
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None, example="abc123")
    message: str = Field(..., min_length=1, example="What courses does Codenixia offer?")
    user_name: Optional[str] = Field(None, example="Rahul")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_001",
                "message": "Tell me about the AI internship program",
                "user_name": "Rahul"
            }
        }


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    timestamp: datetime
    tokens_used: Optional[int] = None


class ChatHistory(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime


# ─── Automation Schemas ────────────────────────────────────────────────────────

class AutomationLog(BaseModel):
    workflow: str
    trigger: str
    status: str
    details: Optional[dict] = None
    created_at: datetime


class AutomationTrigger(BaseModel):
    workflow: str = Field(..., example="lead_notification")
    payload: Optional[dict] = Field(default={})


# ─── Dashboard Schemas ────────────────────────────────────────────────────────

class DashboardStats(BaseModel):
    total_leads: int
    new_leads: int
    converted_leads: int
    total_chat_sessions: int
    total_messages: int
    automation_runs: int
    leads_by_source: dict
    leads_by_status: dict
    recent_leads: List[dict]
    recent_chats: List[dict]
