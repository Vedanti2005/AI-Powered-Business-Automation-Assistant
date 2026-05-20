from fastapi import APIRouter
from datetime import datetime, timezone, timedelta

from database import get_db

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats():
    """
    Admin dashboard: aggregated stats, recent leads, chat sessions, automation logs.
    """
    db = get_db()

    # Lead counts
    total_leads = await db.leads.count_documents({})
    new_leads = await db.leads.count_documents({"status": "new"})
    converted_leads = await db.leads.count_documents({"status": "converted"})
    contacted_leads = await db.leads.count_documents({"status": "contacted"})
    qualified_leads = await db.leads.count_documents({"status": "qualified"})

    # Chat stats
    total_sessions = await db.chat_sessions.count_documents({})
    total_messages = 0
    async for session in db.chat_sessions.find({}, {"messages": 1}):
        total_messages += len(session.get("messages", []))

    # Automation runs
    automation_runs = await db.automation_logs.count_documents({})
    automation_success = await db.automation_logs.count_documents({"status": "success"})

    # Leads by source
    leads_by_source = {}
    async for item in db.leads.aggregate([
        {"$group": {"_id": "$source", "count": {"$sum": 1}}}
    ]):
        leads_by_source[item["_id"] or "unknown"] = item["count"]

    # Leads by status
    leads_by_status = {
        "new": new_leads,
        "contacted": contacted_leads,
        "qualified": qualified_leads,
        "converted": converted_leads,
    }

    # Leads over time (last 7 days)
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    leads_over_time = []
    async for item in db.leads.aggregate([
        {"$match": {"created_at": {"$gte": seven_days_ago}}},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]):
        leads_over_time.append({"date": item["_id"], "count": item["count"]})

    # Recent leads (last 5)
    recent_leads = []
    async for lead in db.leads.find({}, {"name": 1, "email": 1, "status": 1, "source": 1, "course_interest": 1, "created_at": 1}).sort("created_at", -1).limit(5):
        lead["id"] = str(lead["_id"])
        del lead["_id"]
        recent_leads.append(lead)

    # Recent chat sessions (last 5)
    recent_chats = []
    async for s in db.chat_sessions.find(
        {},
        {"session_id": 1, "user_name": 1, "updated_at": 1, "messages": {"$slice": -1}}
    ).sort("updated_at", -1).limit(5):
        s["_id"] = str(s["_id"])
        recent_chats.append(s)

    # Recent automation logs (last 10)
    recent_automations = []
    async for log in db.automation_logs.find({}).sort("created_at", -1).limit(10):
        log["_id"] = str(log["_id"])
        recent_automations.append(log)

    return {
        "leads": {
            "total": total_leads,
            "new": new_leads,
            "contacted": contacted_leads,
            "qualified": qualified_leads,
            "converted": converted_leads,
            "by_source": leads_by_source,
            "by_status": leads_by_status,
            "over_time": leads_over_time,
        },
        "chat": {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
        },
        "automation": {
            "total_runs": automation_runs,
            "successful_runs": automation_success,
        },
        "recent_leads": recent_leads,
        "recent_chats": recent_chats,
        "recent_automations": recent_automations,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }


@router.get("/leads/export")
async def export_leads_csv():
    """Export all leads as CSV data."""
    from fastapi.responses import StreamingResponse
    import csv
    import io

    db = get_db()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Email", "Phone", "Company", "Course Interest", "Source", "Status", "Message", "Created At"])

    async for lead in db.leads.find({}).sort("created_at", -1):
        writer.writerow([
            str(lead["_id"]),
            lead.get("name", ""),
            lead.get("email", ""),
            lead.get("phone", ""),
            lead.get("company", ""),
            lead.get("course_interest", ""),
            lead.get("source", ""),
            lead.get("status", ""),
            lead.get("message", ""),
            lead.get("created_at", "").isoformat() if lead.get("created_at") else ""
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=codenixia_leads.csv"}
    )
