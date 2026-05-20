from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone

from database import get_db
from schemas import AutomationTrigger
from services.gemini_service import get_ai_response

router = APIRouter()

AVAILABLE_WORKFLOWS = [
    "lead_capture",
    "lead_notification",
    "chatbot_interaction",
    "lead_followup_reminder",
    "bulk_lead_summary"
]


@router.get("/workflows")
async def list_workflows():
    """List all available automation workflows."""
    return {
        "workflows": [
            {
                "id": "lead_capture",
                "name": "Lead Capture",
                "description": "Triggered when a new lead form is submitted",
                "trigger": "form_submission",
                "actions": ["save_to_db", "generate_ai_summary", "send_admin_email", "send_welcome_email"]
            },
            {
                "id": "lead_notification",
                "name": "Lead Notification",
                "description": "Email notifications for new leads",
                "trigger": "lead_capture_complete",
                "actions": ["send_admin_notification", "send_user_welcome"]
            },
            {
                "id": "chatbot_interaction",
                "name": "Chatbot Interaction Logger",
                "description": "Logs all chatbot interactions for analytics",
                "trigger": "user_message",
                "actions": ["log_interaction", "store_session"]
            },
            {
                "id": "bulk_lead_summary",
                "name": "Bulk Lead AI Summary",
                "description": "Generate AI summaries for all leads missing them",
                "trigger": "manual",
                "actions": ["fetch_leads", "generate_ai_summaries", "update_db"]
            }
        ]
    }


@router.post("/trigger")
async def trigger_workflow(trigger: AutomationTrigger):
    """Manually trigger an automation workflow."""
    db = get_db()
    now = datetime.now(timezone.utc)

    if trigger.workflow not in AVAILABLE_WORKFLOWS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown workflow. Available: {AVAILABLE_WORKFLOWS}"
        )

    result = {"workflow": trigger.workflow, "status": "triggered", "details": {}}

    # ── Workflow: bulk_lead_summary ──────────────────────────────────────
    if trigger.workflow == "bulk_lead_summary":
        leads_updated = 0
        async for lead in db.leads.find({"ai_summary": None}):
            try:
                from services.gemini_service import generate_lead_summary
                summary = await generate_lead_summary(lead)
                await db.leads.update_one(
                    {"_id": lead["_id"]},
                    {"$set": {"ai_summary": summary}}
                )
                leads_updated += 1
            except Exception as e:
                print(f"Failed summary for {lead.get('email')}: {e}")

        result["details"] = {"leads_updated": leads_updated}
        result["status"] = "completed"

    # ── Workflow: lead_followup_reminder ─────────────────────────────────
    elif trigger.workflow == "lead_followup_reminder":
        from datetime import timedelta
        from services.email_service import send_email

        cutoff = now - timedelta(hours=24)
        count = 0
        async for lead in db.leads.find({"status": "new", "created_at": {"$lte": cutoff}}):
            send_email(
                to_email=lead.get("email"),
                subject="Still interested in Codenixia? Let's connect!",
                html_body=f"<p>Hi {lead.get('name')}, we noticed you signed up but haven't heard back. We'd love to chat!</p>"
            )
            count += 1

        result["details"] = {"reminders_sent": count}
        result["status"] = "completed"

    else:
        result["status"] = "acknowledged"
        result["details"] = {"message": f"Workflow '{trigger.workflow}' acknowledged. It runs automatically on its trigger event."}

    # Log the manual trigger
    await db.automation_logs.insert_one({
        "workflow": trigger.workflow,
        "trigger": "manual_trigger",
        "status": result["status"],
        "details": result["details"],
        "created_at": now
    })

    return result


@router.get("/logs")
async def get_automation_logs(
    workflow: str = None,
    status: str = None,
    limit: int = 50,
    skip: int = 0
):
    """Get automation execution logs."""
    db = get_db()

    query = {}
    if workflow:
        query["workflow"] = workflow
    if status:
        query["status"] = status

    cursor = db.automation_logs.find(query).sort("created_at", -1).skip(skip).limit(limit)
    logs = []
    async for log in cursor:
        log["_id"] = str(log["_id"])
        logs.append(log)

    total = await db.automation_logs.count_documents(query)
    return {"logs": logs, "total": total, "skip": skip, "limit": limit}


@router.get("/logs/stats")
async def automation_stats():
    """Get automation performance statistics."""
    db = get_db()

    stats = {}
    async for item in db.automation_logs.aggregate([
        {"$group": {
            "_id": {"workflow": "$workflow", "status": "$status"},
            "count": {"$sum": 1}
        }}
    ]):
        wf = item["_id"]["workflow"]
        st = item["_id"]["status"]
        if wf not in stats:
            stats[wf] = {}
        stats[wf][st] = item["count"]

    return {"workflow_stats": stats}
