✅ # SETUP CHECKLIST - Codenixia Business Bot

## ✨ Project Structure Fixed!

Your project has been reorganized with the proper structure:

```
business bot/
├── 📁 routers/                    ✅ NEW - API route handlers
│   ├── chat.py
│   ├── leads.py
│   ├── dashboard.py
│   ├── automation.py
│   └── __init__.py
├── 📁 services/                   ✅ NEW - External service integrations
│   ├── gemini_service.py          (Google Gemini AI)
│   ├── email_service.py           (SMTP Email)
│   └── __init__.py
├── 📋 main.py                     ✅ FastAPI entry point
├── 📋 database.py                 ✅ MongoDB async connection
├── 📋 schemas.py                  ✅ Pydantic data models
├── 📄 requirements.txt            ✅ Python dependencies
├── 📝 .env                        ✅ NEW - Environment config (EDIT THIS!)
├── 📖 SETUP.md                    ✅ NEW - Detailed setup guide
├── 🐳 docker-compose.yml          ✅ Multi-container orchestration
├── 🐳 Dockerfile                  ✅ Container image config
└── env.example                    ✅ Template (keep for reference)
```

---

## 🚀 QUICKSTART (Choose One)

### ⭐ Option A: Docker Compose (Recommended - Easiest)

```bash
# 1. Edit .env file with your API keys
# 2. Run:
docker-compose up --build

# Services start at:
# - API:              http://localhost:8000
# - API Docs:         http://localhost:8000/docs
# - MongoDB Express:  http://localhost:8081 (admin / admin123)
```

**Pros**: Everything containerized, no local MongoDB needed  
**Cons**: Requires Docker installation

---

### 2️⃣ Option B: Manual Setup (Local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Edit .env file with your API keys

# 3. Start MongoDB (choose one):
# Option A: Docker
docker run -d -p 27017:27017 mongo:7.0

# Option B: Windows Service (if installed)
net start MongoDB

# 4. Run FastAPI server
uvicorn main:app --reload --port 8000

# Access at: http://localhost:8000/docs
```

---

## 📋 REQUIRED CONFIGURATION

### 1. Edit `.env` file:

```env
# ✏️ MUST CONFIGURE:

# Get from: https://aistudio.google.com/apikey
GEMINI_API_KEY=your_key_here

# Gmail with App Password (for email notifications)
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=xxxx_xxxx_xxxx_xxxx

ADMIN_EMAIL=admin@company.com
```

### 2. Database Choice:

**Local MongoDB:**
```bash
docker run -d -p 27017:27017 mongo:7.0
```

**OR MongoDB Atlas (Cloud):**
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

---

## ✅ VERIFICATION CHECKLIST

- [ ] Edit `.env` with Gemini API key
- [ ] Edit `.env` with SMTP credentials (or skip for dev)
- [ ] Start MongoDB (Docker or local)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run server: `uvicorn main:app --reload`
- [ ] Visit http://localhost:8000/docs
- [ ] Click "Try it out" on any endpoint
- [ ] Test health check: `GET /health`

---

## 🧪 TEST ENDPOINTS

### 1. Health Check (No Auth Needed)
```bash
curl http://localhost:8000/health
```

### 2. Chat with AI
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message":"What is Codenixia?","user_name":"Test"}'
```

### 3. Submit Lead (Triggers Automation)
```bash
curl -X POST http://localhost:8000/api/leads/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name":"John Doe",
    "email":"john@test.com",
    "phone":"9876543210",
    "company":"Tech Corp",
    "course_interest":"AI/LLM",
    "message":"I am interested",
    "source":"website"
  }'
```

### 4. Dashboard Stats
```bash
curl http://localhost:8000/api/dashboard/stats
```

---

## 🆘 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| MongoDB connection error | Start MongoDB with Docker: `docker run -d -p 27017:27017 mongo:7.0` |
| Gemini API error | Get key from https://aistudio.google.com/apikey and add to .env |
| Port 8000 in use | Kill process: `netstat -ano \| findstr :8000` then `taskkill /PID <PID> /F` |
| Email not sending | It's optional! Skip if not configured. Enable in .env to test. |
| Import errors | Run: `pip install -r requirements.txt` |

---

## 📚 DOCUMENTATION

- **Full Setup Guide**: See `SETUP.md`
- **API Docs (Interactive)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🎯 NEXT STEPS

1. ✏️ **Configure .env** (add your API keys)
2. 🗄️ **Start MongoDB** (Docker or local)
3. 📦 **Install dependencies** (`pip install -r requirements.txt`)
4. 🚀 **Run the app** (`uvicorn main:app --reload`)
5. 🧪 **Test endpoints** (visit http://localhost:8000/docs)
6. 🔧 **Customize** (edit prompts in `services/gemini_service.py`)

---

## 📞 SUPPORT

For detailed instructions, see: `SETUP.md`

**You're all set! Happy coding! 🚀**
