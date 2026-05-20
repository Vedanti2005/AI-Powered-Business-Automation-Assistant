from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId

from database import get_db
from schemas import LeadCreate, LeadUpdate, LeadResponse, LeadStatus
from services.gemini_service import generate_lead_summary
from services.email_service import notify_new_lead

router = APIRouter()


def serialize_lead(lead: dict) -> dict:
    lead["id"] = str(lead["_id"])
    del lead["_id"]
    return lead


@router.post("/submit", status_code=201)
async def submit_lead(lead: LeadCreate, background_tasks: BackgroundTasks):
    """
    Submit a new lead (form submission).
    Triggers: email notification + AI summary generation automation.
    """
    db = get_db()
    now = datetime.now(timezone.utc)

    # Check for duplicate email
    existing = await db.leads.find_one({"email": lead.email})
    if existing:
        raise HTTPException(
            status_code=409,
            detail="A lead with this email already exists."
        )

    lead_doc = {
        **lead.model_dump(),
        "status": LeadStatus.NEW,
        "created_at": now,
        "updated_at": now,
        "ai_summary": None,
        "notes": ""
    }

    result = await db.leads.insert_one(lead_doc)
    lead_doc["_id"] = result.inserted_id

    # Log automation event
    await db.automation_logs.insert_one({
        "workflow": "lead_capture",
        "trigger": "form_submission",
        "status": "success",
        "details": {"lead_id": str(result.inserted_id), "email": lead.email},
        "created_at": now
    })

    # Run automation in background: AI summary + email notifications
    background_tasks.add_task(run_lead_automation, lead_doc, str(result.inserted_id))

    return {
        "message": "Lead submitted successfully! We'll be in touch soon.",
        "lead_id": str(result.inserted_id),
        "status": "new"
    }


async def run_lead_automation(lead_doc: dict, lead_id: str):
    """Background task: generate AI summary and send emails."""
    db = get_db()
    try:
        # Generate AI summary using Gemini
        ai_summary = await generate_lead_summary(lead_doc)

        # Update lead with AI summary
        await db.leads.update_one(
            {"_id": ObjectId(lead_id)},
            {"$set": {"ai_summary": ai_summary}}
        )

        # Send email notifications
        email_results = await notify_new_lead(lead_doc, ai_summary)

        # Log automation result
        await db.automation_logs.insert_one({
            "workflow": "lead_notification",
            "trigger": "lead_capture_complete",
            "status": "success",
            "details": {
                "lead_id": lead_id,
                "email_results": email_results,
                "ai_summary_generated": bool(ai_summary)
            },
            "created_at": datetime.now(timezone.utc)
        })

    except Exception as e:
        await db.automation_logs.insert_one({
            "workflow": "lead_notification",
            "trigger": "lead_capture_complete",
            "status": "error",
            "details": {"lead_id": lead_id, "error": str(e)},
            "created_at": datetime.now(timezone.utc)
        })


@router.get("/", )
async def list_leads(
    status: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    """List all leads with optional filters (admin)."""
    db = get_db()

    query = {}
    if status:
        query["status"] = status
    if source:
        query["source"] = source

    cursor = db.leads.find(query).sort("created_at", -1).skip(skip).limit(limit)
    leads = []
    async for lead in cursor:
        leads.append(serialize_lead(lead))

    total = await db.leads.count_documents(query)
    return {"leads": leads, "total": total, "skip": skip, "limit": limit}


@router.get("/{lead_id}")
async def get_lead(lead_id: str):
    """Get a single lead by ID."""
    db = get_db()
    try:
        lead = await db.leads.find_one({"_id": ObjectId(lead_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid lead ID")

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return serialize_lead(lead)


@router.patch("/{lead_id}")
async def update_lead(lead_id: str, update: LeadUpdate):
    """Update lead status or notes (admin)."""
    db = get_db()
    try:
        oid = ObjectId(lead_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid lead ID")

    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    update_data["updated_at"] = datetime.now(timezone.utc)

    result = await db.leads.update_one({"_id": oid}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lead not found")

    updated = await db.leads.find_one({"_id": oid})
    return serialize_lead(updated)


@router.delete("/{lead_id}")
async def delete_lead(lead_id: str):
    """Delete a lead (admin)."""
    db = get_db()
    try:
        result = await db.leads.delete_one({"_id": ObjectId(lead_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid lead ID")

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Lead not found")

    return {"message": "Lead deleted", "lead_id": lead_id}
