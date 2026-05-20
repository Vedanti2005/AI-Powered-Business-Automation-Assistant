import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@codenixia.com")


def send_email(to_email: str, subject: str, html_body: str, text_body: Optional[str] = None) -> bool:
    """Send an email notification."""
    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"⚠️  Email not configured. Would send to {to_email}: {subject}")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Codenixia AI <{SMTP_USER}>"
        msg["To"] = to_email

        if text_body:
            msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())

        print(f"✅ Email sent to {to_email}")
        return True

    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


def build_lead_notification_html(lead: dict) -> str:
    return f"""
    <html><body style="font-family: Arial, sans-serif; padding: 20px;">
    <h2 style="color: #2563eb;">🎯 New Lead Captured - Codenixia</h2>
    <table style="border-collapse: collapse; width: 100%;">
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Name</b></td><td style="padding: 8px; border: 1px solid #ddd;">{lead.get('name')}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Email</b></td><td style="padding: 8px; border: 1px solid #ddd;">{lead.get('email')}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Phone</b></td><td style="padding: 8px; border: 1px solid #ddd;">{lead.get('phone', 'N/A')}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Company</b></td><td style="padding: 8px; border: 1px solid #ddd;">{lead.get('company', 'N/A')}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Interest</b></td><td style="padding: 8px; border: 1px solid #ddd;">{lead.get('course_interest', 'N/A')}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Message</b></td><td style="padding: 8px; border: 1px solid #ddd;">{lead.get('message', 'N/A')}</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Source</b></td><td style="padding: 8px; border: 1px solid #ddd;">{lead.get('source', 'N/A')}</td></tr>
    </table>
    <p style="color: #888; margin-top: 20px;">Codenixia AI System • Auto-generated</p>
    </body></html>
    """


def build_lead_welcome_html(lead: dict, ai_summary: str = "") -> str:
    return f"""
    <html><body style="font-family: Arial, sans-serif; padding: 20px; max-width: 600px;">
    <h2 style="color: #2563eb;">👋 Welcome to Codenixia, {lead.get('name')}!</h2>
    <p>Thank you for your interest in our <b>{lead.get('course_interest', 'AI/LLM Automation')}</b> program.</p>
    {f'<p>{ai_summary}</p>' if ai_summary else ''}
    <p>Our team will reach out within <b>24 hours</b> to guide you through the next steps.</p>
    <div style="background: #f0f7ff; padding: 15px; border-radius: 8px; margin: 20px 0;">
        <b>What to expect:</b>
        <ul>
            <li>Program overview call</li>
            <li>Project details & timeline</li>
            <li>Onboarding instructions</li>
        </ul>
    </div>
    <p>Meanwhile, feel free to chat with our AI assistant anytime!</p>
    <p style="color: #888;">Team Codenixia</p>
    </body></html>
    """


async def notify_new_lead(lead: dict, ai_summary: str = "") -> dict:
    """Send notifications when a new lead is captured."""
    results = {}

    # Notify admin
    admin_html = build_lead_notification_html(lead)
    results["admin_notified"] = send_email(
        to_email=ADMIN_EMAIL,
        subject=f"🎯 New Lead: {lead.get('name')} - {lead.get('course_interest', 'General')}",
        html_body=admin_html
    )

    # Send welcome email to lead
    welcome_html = build_lead_welcome_html(lead, ai_summary)
    results["welcome_sent"] = send_email(
        to_email=lead.get("email"),
        subject="Welcome to Codenixia – Your AI Internship Journey Begins!",
        html_body=welcome_html
    )

    return results
