# 🚀 Codenixia Business Bot - Setup Guide

## 📋 Requirements

- **Python**: 3.11+
- **MongoDB**: 5.0+ (local or Atlas cloud)
- **Docker** (optional, for containerized setup)
- **Gemini API Key**: From Google AI Studio
- **Gmail Account** (optional, for email notifications)

---

## ⚙️ Option 1: Local Setup (Manual)

### Step 1: Install Python Dependencies

```bash
cd "e:\mini project\business bot"
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

Edit the `.env` file in the project root:

```env
# MongoDB
MONGO_URI=mongodb://localhost:27017
DB_NAME=codenixia_db

# Gemini AI (Get from: https://aistudio.google.com/apikey)
GEMINI_API_KEY=your_actual_api_key_here

# Email Configuration (Gmail with App Password)
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
ADMIN_EMAIL=admin@codenixia.com

# App Config
APP_ENV=development
SECRET_KEY=change_this_to_random_key
```

### Step 3: Start MongoDB Locally

**Option A: MongoDB Community (Windows)**
```bash
# If installed via MSI, it runs as a service. Start it:
net start MongoDB

# Or if installed via Chocolatey:
mongod
```

**Option B: Docker Container**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

### Step 4: Run the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: **http://localhost:8000**
- API Docs (Swagger): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🐳 Option 2: Docker Compose Setup (Recommended)

This sets up MongoDB + MongoDB Express + FastAPI in containers.

### Prerequisites

- Docker & Docker Compose installed

### Step 1: Configure Environment

Update `.env` file with your API keys:

```env
GEMINI_API_KEY=your_actual_key_here
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
ADMIN_EMAIL=admin@codenixia.com
```

### Step 2: Start All Services

```bash
cd "e:\mini project\business bot"
docker-compose up --build
```

### Step 3: Access Services

| Service | URL | Login |
|---------|-----|-------|
| FastAPI API | http://localhost:8000 | — |
| API Docs | http://localhost:8000/docs | — |
| MongoDB Express | http://localhost:8081 | admin / admin123 |

---

## 🧪 Testing the API

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Chat with AI
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Codenixia?",
    "user_name": "John"
  }'
```

### 3. Submit a Lead
```bash
curl -X POST http://localhost:8000/api/leads/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "9876543210",
    "company": "Tech Corp",
    "course_interest": "AI/LLM",
    "message": "I want to learn AI",
    "source": "website"
  }'
```

### 4. Get Dashboard Stats
```bash
curl http://localhost:8000/api/dashboard/stats
```

---

## 📱 Project Structure

```
.
├── main.py                  # FastAPI entry point
├── database.py              # MongoDB async connection
├── schemas.py               # Pydantic models
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── routers/
│   ├── chat.py              # AI Chat endpoints
│   ├── leads.py             # Lead management
│   ├── dashboard.py         # Admin dashboard
│   └── automation.py        # Workflow automation
├── services/
│   ├── gemini_service.py    # Gemini AI integration
│   └── email_service.py     # Email notifications
├── Dockerfile               # Container image
├── docker-compose.yml       # Multi-container setup
└── README.md               # Documentation
```

---

## 🔑 API Endpoints

### Chat
- `POST /api/chat/message` - Send message to AI
- `GET /api/chat/history/{session_id}` - Get conversation history
- `DELETE /api/chat/history/{session_id}` - Clear session
- `GET /api/chat/sessions` - List all sessions

### Leads
- `POST /api/leads/submit` - Submit new lead
- `GET /api/leads/` - List all leads
- `GET /api/leads/{lead_id}` - Get lead details
- `PATCH /api/leads/{lead_id}` - Update lead
- `DELETE /api/leads/{lead_id}` - Delete lead

### Dashboard
- `GET /api/dashboard/stats` - Get statistics
- `GET /api/dashboard/leads/export` - Export leads as CSV

### Automation
- `GET /api/automation/workflows` - List workflows
- `POST /api/automation/trigger` - Trigger automation
- `GET /api/automation/logs` - Get automation logs

---

## ⚙️ Configuration

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `MONGO_URI` | MongoDB connection | `mongodb://localhost:27017` |
| `DB_NAME` | Database name | `codenixia_db` |
| `GEMINI_API_KEY` | Google Gemini API key | `AIza...` |
| `SMTP_USER` | Sender email | `bot@gmail.com` |
| `SMTP_PASSWORD` | Email app password | `xxxx xxxx xxxx xxxx` |
| `ADMIN_EMAIL` | Admin notification email | `admin@codenixia.com` |
| `APP_ENV` | Environment | `development` |
| `SECRET_KEY` | JWT secret | `your-secret-key` |

---

## 🛠️ Troubleshooting

### MongoDB Connection Error
```
Error: pymongo.errors.ServerSelectionTimeoutError
```
**Solution**: Ensure MongoDB is running
```bash
# Check if MongoDB is running
mongosh

# Or start Docker container
docker run -d -p 27017:27017 mongo:7.0
```

### Gemini API Key Error
```
Error: Invalid API key
```
**Solution**: 
1. Go to https://aistudio.google.com/apikey
2. Create a new API key
3. Update `.env` file

### Port Already in Use
```
Error: Address already in use :::8000
```
**Solution**: Kill process or use different port
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn main:app --port 8001
```

### Email Not Sending
```
⚠️ Email not configured
```
**Solution**: Gmail setup
1. Enable 2-Step Verification
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Update `.env` with app password (16-char)

---

## 📊 Monitoring & Logs

### View Application Logs
```bash
# With timestamp
uvicorn main:app --log-level debug

# Save to file
uvicorn main:app > app.log 2>&1
```

### Monitor MongoDB
```bash
# Using mongosh
mongosh
> db.leads.find()
> db.chat_sessions.count()
```

### Docker Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f mongo
```

---

## 🚀 Deployment Tips

1. **Use MongoDB Atlas** (cloud) instead of local MongoDB
2. **Enable HTTPS** in production
3. **Set proper SECRET_KEY** (use `secrets.token_urlsafe()`)
4. **Configure CORS** for your frontend domain
5. **Rate limiting** for public endpoints
6. **Add authentication** for admin routes

---

## ❓ FAQ

**Q: How do I change the database name?**  
A: Update `DB_NAME` in `.env`

**Q: Can I use MySQL instead of MongoDB?**  
A: No, this app is built for MongoDB. You'd need to rewrite the database layer.

**Q: How do I add more routes?**  
A: Create files in `routers/` and import them in `main.py`

**Q: Is email optional?**  
A: Yes, without SMTP config, email notifications are skipped (with warning)

---

## 📝 Next Steps

1. ✅ Set up `.env` with API keys
2. ✅ Start MongoDB (local or Docker)
3. ✅ Install dependencies: `pip install -r requirements.txt`
4. ✅ Run app: `uvicorn main:app --reload`
5. ✅ Test endpoints at http://localhost:8000/docs
6. ✅ Customize AI prompts in `services/gemini_service.py`

---

**Happy coding! 🚀 Codenixia**
