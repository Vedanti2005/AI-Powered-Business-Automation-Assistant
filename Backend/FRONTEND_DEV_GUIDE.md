# 🎨 Frontend Development Guide - Codenixia Business Bot

A comprehensive guide for frontend developers to build the UI for the Codenixia Business Bot application.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [API Base URL](#api-base-url)
3. [API Endpoints](#api-endpoints)
4. [Data Models](#data-models)
5. [Response Formats](#response-formats)
6. [Frontend Components](#frontend-components)
7. [Setup Instructions](#setup-instructions)
8. [Examples](#examples)
9. [Error Handling](#error-handling)

---

## 🎯 Overview

**Codenixia Business Bot** is an AI-powered assistant that:
- Handles multi-turn conversations via **AI Chatbot**
- Captures leads through **Lead Form**
- Tracks lead status and analytics
- Automates workflows (email notifications, AI summaries)
- Provides admin dashboard with statistics

**Tech Stack:**
- Backend: FastAPI (Python)
- Database: MongoDB
- AI: Google Gemini 1.5 Flash
- Frontend: React / Vue / Angular (Your Choice)

---

## 🔗 API Base URL

```
http://localhost:8000
```

**Interactive API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 📡 API Endpoints

### 1. HEALTH CHECK (No Auth)

#### GET `/health`
Check if the backend is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "codenixia-backend"
}
```

**cURL:**
```bash
curl http://localhost:8000/health
```

---

### 2. CHAT ENDPOINTS

#### POST `/api/chat/message`
Send a message to the AI chatbot.

**Request Body:**
```json
{
  "session_id": "session_123",  // Optional - auto-generated if not provided
  "message": "What is Codenixia?",
  "user_name": "Rahul"  // Optional
}
```

**Response:**
```json
{
  "session_id": "session_123",
  "reply": "Codenixia is an ed-tech company offering AI/LLM internship programs...",
  "timestamp": "2024-05-19T10:30:45.123Z",
  "tokens_used": null
}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What courses do you offer?",
    "user_name": "John"
  }'
```

---

#### GET `/api/chat/history/{session_id}`
Get full conversation history for a session.

**Response:**
```json
{
  "session_id": "session_123",
  "messages": [
    {
      "role": "user",
      "content": "What is Codenixia?",
      "timestamp": "2024-05-19T10:30:00Z"
    },
    {
      "role": "model",
      "content": "Codenixia is...",
      "timestamp": "2024-05-19T10:30:05Z"
    }
  ],
  "created_at": "2024-05-19T10:30:00Z",
  "updated_at": "2024-05-19T10:30:05Z"
}
```

**cURL:**
```bash
curl http://localhost:8000/api/chat/history/session_123
```

---

#### DELETE `/api/chat/history/{session_id}`
Clear/reset a chat session.

**Response:**
```json
{
  "message": "Session cleared",
  "session_id": "session_123"
}
```

---

#### GET `/api/chat/sessions?limit=20&skip=0`
List all chat sessions (admin view).

**Query Parameters:**
- `limit` (int): Results per page (default: 20)
- `skip` (int): Results to skip (default: 0)

**Response:**
```json
{
  "sessions": [
    {
      "session_id": "abc123",
      "user_name": "John Doe",
      "created_at": "2024-05-19T10:00:00Z",
      "updated_at": "2024-05-19T10:30:00Z",
      "messages": [
        {
          "role": "user",
          "content": "Last message..."
        }
      ]
    }
  ],
  "total": 45,
  "skip": 0,
  "limit": 20
}
```

---

### 3. LEAD MANAGEMENT ENDPOINTS

#### POST `/api/leads/submit`
Submit a new lead (form submission).

**Request Body:**
```json
{
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "phone": "+91-9876543210",
  "company": "Tech Startup",
  "course_interest": "AI/LLM",
  "message": "I am interested in the internship program",
  "source": "website"
}
```

**Response:**
```json
{
  "message": "Lead submitted successfully! We'll be in touch soon.",
  "lead_id": "507f1f77bcf86cd799439011",
  "status": "new"
}
```

**Field Validations:**
- `name`: Required, 2-100 characters
- `email`: Required, valid email format
- `phone`: Optional, any format
- `company`: Optional
- `course_interest`: Optional
- `message`: Optional
- `source`: Required, one of: "website", "chatbot", "form", "referral"

**cURL:**
```bash
curl -X POST http://localhost:8000/api/leads/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "company": "Tech Corp",
    "course_interest": "AI/LLM",
    "message": "Interested",
    "source": "website"
  }'
```

---

#### GET `/api/leads/?status=new&source=website&limit=20&skip=0`
List all leads with optional filters.

**Query Parameters:**
- `status` (string): Filter by status - "new", "contacted", "qualified", "converted", "rejected"
- `source` (string): Filter by source - "website", "chatbot", "form", "referral"
- `limit` (int): Results per page
- `skip` (int): Results to skip

**Response:**
```json
{
  "leads": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Rahul Sharma",
      "email": "rahul@example.com",
      "phone": "+91-9876543210",
      "company": "Tech Startup",
      "message": "Interested in AI program",
      "source": "website",
      "status": "new",
      "course_interest": "AI/LLM",
      "created_at": "2024-05-19T10:00:00Z",
      "updated_at": "2024-05-19T10:00:00Z"
    }
  ],
  "total": 150,
  "skip": 0,
  "limit": 20
}
```

---

#### GET `/api/leads/{lead_id}`
Get a single lead by ID.

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "phone": "+91-9876543210",
  "company": "Tech Startup",
  "message": "Interested",
  "source": "website",
  "status": "new",
  "course_interest": "AI/LLM",
  "created_at": "2024-05-19T10:00:00Z",
  "updated_at": "2024-05-19T10:00:00Z"
}
```

---

#### PATCH `/api/leads/{lead_id}`
Update lead status or notes.

**Request Body:**
```json
{
  "status": "contacted",
  "notes": "Called at 3 PM, interested in Full-Stack program"
}
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "status": "contacted",
  "notes": "Called at 3 PM...",
  "updated_at": "2024-05-19T10:30:00Z"
}
```

---

#### DELETE `/api/leads/{lead_id}`
Delete a lead.

**Response:**
```json
{
  "message": "Lead deleted",
  "lead_id": "507f1f77bcf86cd799439011"
}
```

---

### 4. DASHBOARD ENDPOINTS

#### GET `/api/dashboard/stats`
Get aggregated dashboard statistics and analytics.

**Response:**
```json
{
  "leads": {
    "total": 150,
    "new": 45,
    "contacted": 30,
    "qualified": 20,
    "converted": 55,
    "by_source": {
      "website": 80,
      "chatbot": 50,
      "form": 20
    },
    "by_status": {
      "new": 45,
      "contacted": 30,
      "qualified": 20,
      "converted": 55
    },
    "over_time": [
      {
        "date": "2024-05-13",
        "count": 12
      },
      {
        "date": "2024-05-14",
        "count": 18
      }
    ]
  },
  "chat": {
    "total_sessions": 280,
    "total_messages": 1450
  },
  "automation": {
    "total_runs": 500,
    "successful_runs": 485
  },
  "recent_leads": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "John Doe",
      "email": "john@example.com",
      "status": "new",
      "source": "website",
      "course_interest": "AI/LLM",
      "created_at": "2024-05-19T15:30:00Z"
    }
  ],
  "recent_chats": [
    {
      "session_id": "session_123",
      "user_name": "Rahul",
      "updated_at": "2024-05-19T15:25:00Z",
      "messages": [
        {
          "role": "user",
          "content": "Last message..."
        }
      ]
    }
  ],
  "recent_automations": [
    {
      "workflow": "lead_capture",
      "trigger": "form_submission",
      "status": "success",
      "details": {
        "lead_id": "507f1f77bcf86cd799439011",
        "email": "john@example.com"
      },
      "created_at": "2024-05-19T15:00:00Z"
    }
  ],
  "generated_at": "2024-05-19T15:30:45.123Z"
}
```

---

#### GET `/api/dashboard/leads/export`
Export all leads as CSV file.

**Response:** CSV file download
```
ID,Name,Email,Phone,Company,Course Interest,Source,Status,Message,Created At
507f1f77bcf86cd799439011,Rahul Sharma,rahul@example.com,+91-9876543210,Tech Startup,AI/LLM,website,new,Interested,2024-05-19T10:00:00Z
```

---

### 5. AUTOMATION ENDPOINTS

#### GET `/api/automation/workflows`
List all available automation workflows.

**Response:**
```json
{
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
```

---

#### POST `/api/automation/trigger`
Manually trigger an automation workflow.

**Request Body:**
```json
{
  "workflow": "bulk_lead_summary"
}
```

**Response:**
```json
{
  "workflow": "bulk_lead_summary",
  "status": "completed",
  "details": {
    "leads_updated": 12
  }
}
```

---

#### GET `/api/automation/logs?workflow=lead_capture&status=success&limit=50&skip=0`
Get automation execution logs.

**Query Parameters:**
- `workflow` (string): Filter by workflow name
- `status` (string): Filter by status - "success", "error", "pending"
- `limit` (int): Results per page
- `skip` (int): Results to skip

**Response:**
```json
{
  "logs": [
    {
      "workflow": "lead_capture",
      "trigger": "form_submission",
      "status": "success",
      "details": {
        "lead_id": "507f1f77bcf86cd799439011",
        "email": "john@example.com"
      },
      "created_at": "2024-05-19T15:00:00Z"
    }
  ],
  "total": 245,
  "skip": 0,
  "limit": 50
}
```

---

#### GET `/api/automation/logs/stats`
Get automation performance statistics.

**Response:**
```json
{
  "workflow_stats": {
    "lead_capture": {
      "success": 480,
      "error": 5
    },
    "lead_notification": {
      "success": 475,
      "error": 8
    },
    "chatbot_interaction": {
      "success": 1450,
      "error": 2
    }
  }
}
```

---

## 📊 Data Models

### Lead Model
```typescript
interface Lead {
  id: string;                 // MongoDB ObjectId as string
  name: string;               // Required, 2-100 chars
  email: string;              // Required, valid email
  phone?: string;             // Optional
  company?: string;           // Optional
  message?: string;           // Optional
  source: "website" | "chatbot" | "form" | "referral";
  status: "new" | "contacted" | "qualified" | "converted" | "rejected";
  course_interest?: string;   // e.g., "AI/LLM", "Full-Stack"
  ai_summary?: string;        // Auto-generated by Gemini
  notes?: string;             // Admin notes
  created_at: string;         // ISO datetime
  updated_at: string;         // ISO datetime
}
```

### Chat Session Model
```typescript
interface ChatSession {
  session_id: string;
  user_name?: string;
  messages: ChatMessage[];
  created_at: string;         // ISO datetime
  updated_at: string;         // ISO datetime
}

interface ChatMessage {
  role: "user" | "model";
  content: string;
  timestamp: string;          // ISO datetime
}
```

### Automation Log Model
```typescript
interface AutomationLog {
  _id: string;
  workflow: string;           // "lead_capture", "lead_notification", etc.
  trigger: string;            // "form_submission", "manual_trigger", etc.
  status: "success" | "error" | "pending";
  details: Record<string, any>;
  created_at: string;         // ISO datetime
}
```

---

## 📦 Response Formats

### Success Response
```json
{
  "data": {},
  "message": "Operation successful",
  "status": 200
}
```

### Error Response
```json
{
  "detail": "Error message describing what went wrong",
  "status": 400  // or 404, 500, etc.
}
```

### Validation Error Response (400)
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

### Not Found Response (404)
```json
{
  "detail": "Lead not found"
}
```

### Server Error Response (500)
```json
{
  "detail": "Internal server error"
}
```

---

## 🎨 Frontend Components

### Recommended Component Structure

```
src/
├── components/
│   ├── Chatbot/
│   │   ├── ChatWindow.jsx           # Main chat UI
│   │   ├── ChatMessage.jsx          # Individual message
│   │   ├── ChatInput.jsx            # Input box
│   │   └── useChat.js               # Custom hook
│   ├── LeadForm/
│   │   ├── LeadForm.jsx             # Form component
│   │   ├── FormField.jsx            # Reusable field
│   │   └── useLeadForm.js           # Form logic
│   ├── Dashboard/
│   │   ├── Dashboard.jsx            # Main dashboard
│   │   ├── StatsCard.jsx            # Stat card component
│   │   ├── LeadsTable.jsx           # Leads list
│   │   ├── Chart.jsx                # Analytics chart
│   │   └── useDashboard.js          # Data fetching
│   ├── Common/
│   │   ├── Navbar.jsx
│   │   ├── Sidebar.jsx
│   │   ├── Loading.jsx
│   │   └── ErrorBoundary.jsx
├── services/
│   ├── api.js                       # API client setup
│   ├── chatService.js               # Chat API calls
│   ├── leadService.js               # Lead API calls
│   ├── dashboardService.js          # Dashboard API calls
│   └── automationService.js         # Automation API calls
├── hooks/
│   ├── useApi.js                    # Reusable API hook
│   └── useLocalStorage.js           # Local storage hook
├── pages/
│   ├── ChatPage.jsx
│   ├── LeadPage.jsx
│   ├── DashboardPage.jsx
│   └── AdminPage.jsx
├── App.jsx
└── index.js
```

---

## 🚀 Setup Instructions

### 1. Create React App (or use your framework)

```bash
npx create-react-app codenixia-frontend
cd codenixia-frontend
npm install axios react-router-dom
```

### 2. Set Up API Client

**`src/services/api.js`:**
```javascript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
```

**`.env`:**
```
REACT_APP_API_URL=http://localhost:8000
```

### 3. Create API Service Modules

**`src/services/chatService.js`:**
```javascript
import api from './api';

export const sendMessage = async (sessionId, message, userName) => {
  const response = await api.post('/api/chat/message', {
    session_id: sessionId,
    message,
    user_name: userName,
  });
  return response.data;
};

export const getChatHistory = async (sessionId) => {
  const response = await api.get(`/api/chat/history/${sessionId}`);
  return response.data;
};

export const listSessions = async (limit = 20, skip = 0) => {
  const response = await api.get('/api/chat/sessions', {
    params: { limit, skip },
  });
  return response.data;
};

export const clearSession = async (sessionId) => {
  const response = await api.delete(`/api/chat/history/${sessionId}`);
  return response.data;
};
```

**`src/services/leadService.js`:**
```javascript
import api from './api';

export const submitLead = async (leadData) => {
  const response = await api.post('/api/leads/submit', leadData);
  return response.data;
};

export const listLeads = async (status, source, limit = 20, skip = 0) => {
  const response = await api.get('/api/leads/', {
    params: { status, source, limit, skip },
  });
  return response.data;
};

export const getLead = async (leadId) => {
  const response = await api.get(`/api/leads/${leadId}`);
  return response.data;
};

export const updateLead = async (leadId, updateData) => {
  const response = await api.patch(`/api/leads/${leadId}`, updateData);
  return response.data;
};

export const deleteLead = async (leadId) => {
  const response = await api.delete(`/api/leads/${leadId}`);
  return response.data;
};

export const exportLeads = async () => {
  const response = await api.get('/api/dashboard/leads/export', {
    responseType: 'blob',
  });
  return response.data;
};
```

**`src/services/dashboardService.js`:**
```javascript
import api from './api';

export const getDashboardStats = async () => {
  const response = await api.get('/api/dashboard/stats');
  return response.data;
};
```

---

## 📚 Examples

### React Hook Example: Chat Component

```jsx
import React, { useState, useEffect } from 'react';
import { sendMessage, getChatHistory } from '../services/chatService';

function ChatWindow() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [userName, setUserName] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const newSessionId = `session_${Date.now()}`;
    setSessionId(newSessionId);
  }, []);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    try {
      const response = await sendMessage(sessionId, input, userName);
      
      setMessages([
        ...messages,
        { role: 'user', content: input },
        { role: 'model', content: response.reply },
      ]);
      
      setInput('');
    } catch (error) {
      console.error('Chat error:', error);
      alert('Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <p>{msg.content}</p>
          </div>
        ))}
      </div>
      
      <form onSubmit={handleSendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatWindow;
```

### Lead Form Component Example

```jsx
import React, { useState } from 'react';
import { submitLead } from '../services/leadService';

function LeadForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    course_interest: '',
    message: '',
    source: 'website',
  });

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await submitLead(formData);
      setSuccess(true);
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        company: '',
        course_interest: '',
        message: '',
        source: 'website',
      });

      setTimeout(() => setSuccess(false), 3000);
    } catch (error) {
      console.error('Form error:', error);
      alert('Failed to submit. ' + error.response?.data?.detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="lead-form">
      {success && <div className="success">Lead submitted successfully!</div>}

      <input
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="Your Name"
        required
      />

      <input
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
        placeholder="Your Email"
        required
      />

      <input
        type="tel"
        name="phone"
        value={formData.phone}
        onChange={handleChange}
        placeholder="Your Phone"
      />

      <input
        type="text"
        name="company"
        value={formData.company}
        onChange={handleChange}
        placeholder="Your Company"
      />

      <select
        name="course_interest"
        value={formData.course_interest}
        onChange={handleChange}
      >
        <option value="">Select Course Interest</option>
        <option value="AI/LLM">AI/LLM</option>
        <option value="Full-Stack">Full-Stack</option>
        <option value="Python">Python</option>
        <option value="Automation">Automation</option>
      </select>

      <textarea
        name="message"
        value={formData.message}
        onChange={handleChange}
        placeholder="Your Message"
      />

      <button type="submit" disabled={loading}>
        {loading ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}

export default LeadForm;
```

---

## ❌ Error Handling

### Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Lead retrieved successfully |
| 201 | Created | New lead submitted |
| 400 | Bad Request | Invalid email format |
| 404 | Not Found | Lead ID doesn't exist |
| 409 | Conflict | Email already exists |
| 500 | Server Error | Database connection failed |

### Frontend Error Handling Pattern

```javascript
async function handleApiCall(apiFunction) {
  try {
    const data = await apiFunction();
    return { success: true, data };
  } catch (error) {
    if (error.response?.status === 404) {
      return { success: false, message: 'Not found' };
    } else if (error.response?.status === 409) {
      return { success: false, message: 'Already exists' };
    } else if (error.response?.status === 400) {
      return { success: false, message: error.response.data.detail };
    } else {
      return { success: false, message: 'Server error. Try again later.' };
    }
  }
}
```

---

## 🎯 Key Features to Implement

### 1. Chatbot Page
- [ ] Chat message display
- [ ] Auto-scroll to latest message
- [ ] Session management (store in localStorage)
- [ ] User name input
- [ ] Message loading state
- [ ] Error notifications
- [ ] Clear chat history button

### 2. Lead Form Page
- [ ] Form validation
- [ ] Success/error messages
- [ ] Loading state
- [ ] Course interest dropdown
- [ ] Source tracking

### 3. Lead Management (Admin)
- [ ] List all leads with pagination
- [ ] Filter by status/source
- [ ] Search by name/email
- [ ] Edit lead status/notes
- [ ] Delete lead
- [ ] Export to CSV
- [ ] Lead detail modal

### 4. Dashboard (Admin)
- [ ] Key statistics cards (total, new, converted)
- [ ] Lead status pie chart
- [ ] Lead source bar chart
- [ ] Leads over time line chart
- [ ] Recent leads list
- [ ] Recent chat sessions
- [ ] Automation logs
- [ ] Export functionality

### 5. Navigation
- [ ] Navbar with links
- [ ] Sidebar for admin features
- [ ] Mobile responsive menu
- [ ] User session display

---

## 📱 Responsive Design Tips

```css
/* Mobile-first approach */
@media (max-width: 768px) {
  .chat-window {
    height: 100vh;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none; /* Toggle with hamburger menu */
  }
}
```

---

## 🔐 Security Notes

1. **Never store sensitive data** in localStorage (API keys, passwords)
2. **Validate inputs** on both frontend and backend
3. **Handle CORS** properly (backend has * configured)
4. **Use HTTPS** in production
5. **Sanitize HTML** when displaying user content
6. **Implement rate limiting** on critical endpoints

---

## 📞 Backend Support

For any API changes or new features:
1. Check `/docs` endpoint for live documentation
2. Contact backend team for modifications
3. Report bugs with endpoint URL and request/response

---

## 🎬 Getting Started Quick Checklist

- [ ] Backend running at `http://localhost:8000`
- [ ] Test health endpoint: `curl http://localhost:8000/health`
- [ ] Create React app: `npx create-react-app codenixia-frontend`
- [ ] Install dependencies: `npm install axios react-router-dom`
- [ ] Create `.env` file with `REACT_APP_API_URL`
- [ ] Create API service files
- [ ] Build first component (ChatWindow or LeadForm)
- [ ] Test API calls using interactive docs at `/docs`

---

**Happy Frontend Coding! 🚀**

For questions, refer to the backend API docs at: `http://localhost:8000/docs`
