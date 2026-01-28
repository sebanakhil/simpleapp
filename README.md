# Voice Chat Persuasion App - Azure AI Foundry Edition

A web application where users engage in voice conversations with AI agents to practice persuasion skills, with real-time conviction tracking.

## 🚀 Key Features

- 🎤 **Voice Chat with Google Speech Recognition** (free, no API key needed)
- 🤖 **Azure AI Foundry Agents** with persistent conversation threads
- 📊 **Live Conviction Meter** tracking persuasion effectiveness (0-100%)
- 👥 **5 Unique Personas** with different resistance levels
- 💬 **Text Chat Alternative** for testing
- 🔓 **No Login Required** - anonymous conversations

## 📋 Prerequisites

- Python 3.8+
- Azure subscription with:
  - Cosmos DB account
  - Azure AI Foundry project with an agent
- Azure CLI (`az login` completed)

## ⚡ Quick Setup (5 Minutes)

### 1. Install Dependencies
```bash
cd python-app
pip install -r requirements.txt
```

### 2. Azure Login
```bash
az login
```
Required for `DefaultAzureCredential()` to authenticate with Azure AI Foundry.

### 3. Configure `.env`
```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

Required values:
```env
COSMOS_ENDPOINT=https://your-db.documents.azure.com:443/
COSMOS_KEY=your-key
COSMOS_DATABASE=VoiceChatDB

AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
AZURE_AI_AGENT_ID=asst_xxxxxxxxxxxxxxxxxxxxx
```

**Where to find:**
- Cosmos DB: Azure Portal → Your Cosmos DB → Keys
- AI Project Endpoint: Azure AI Foundry → Your Project → Overview  
- Agent ID: Azure AI Foundry → Agents → Your Agent → Copy ID

### 4. Initialize Database
```bash
python seed.py
```

### 5. Run
```bash
python app.py
```

### 6. Open Browser
**http://localhost:5000** 🎉

## 🎯 How It Works

```
User Voice → Google STT → Azure AI Agent → Conviction Analysis → Text Response
                                ↓
                      Cosmos DB (history)
```

### Tech Stack
- **Frontend**: Vanilla JS with beautiful gradient UI
- **Backend**: Flask
- **STT**: Google Speech Recognition (free)
- **AI**: Azure AI Foundry Agents
- **Database**: Cosmos DB

## 📝 API Endpoints

```bash
# Get cases
GET /api/cases

# Create session
POST /api/sessions
{"caseId": "case-swimming-001"}

# Send voice message  
POST /api/chat/{session_id}/message
(multipart/form-data with audio file)

# Send text message
POST /api/chat/{session_id}/text
{"message": "Your persuasive text"}

# End session
POST /api/sessions/{session_id}/end
```

## 🧪 Quick Test

### Text Chat (Easiest)
1. Open http://localhost:5000
2. Click "Convince to Go Swimming"
3. Type: "Swimming is great low-impact exercise!"
4. Watch conviction meter update

### Voice Chat
1. Click 🎤 microphone button
2. Allow browser microphone access
3. Speak: "Swimming is healthy!"
4. Click again to stop
5. See transcription and AI response

### cURL Test
```bash
# Create session
curl -X POST http://localhost:5000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"caseId": "case-swimming-001"}'

# Send message (replace SESSION_ID)
curl -X POST http://localhost:5000/api/chat/SESSION_ID/text \
  -H "Content-Type: application/json" \
  -d '{"message": "Swimming builds endurance!"}'
```

## 🎭 Available Scenarios

1. **Convince to Go Swimming** (Medium)
   - Alex: Busy software engineer
   - Objections: No time, cold water, no gear

2. **Weekend Hiking Trip** (Hard)
   - Sam: Netflix homebody
   - Objections: Exhausting, dangerous

3. **Join a Gym** (Medium)
   - Jordan: Price-conscious
   - Objections: Expensive, never sticks

4. **Learn to Cook** (Easy)
   - Casey: Takeout dependent
   - Objections: No time, complicated

5. **Join a Book Club** (Medium)
   - Riley: Busy parent
   - Objections: No time, anxiety

## 🚀 Deploy to Azure

### Option 1: Quick Deploy Script
```bash
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual Deploy
```bash
# Create Web App
az webapp create \
  --name your-app \
  --resource-group your-rg \
  --plan your-plan \
  --runtime "PYTHON:3.11"

# Enable managed identity
az webapp identity assign \
  --resource-group your-rg \
  --name your-app

# Configure settings
az webapp config appsettings set \
  --name your-app \
  --resource-group your-rg \
  --settings \
    COSMOS_ENDPOINT="..." \
    COSMOS_KEY="..." \
    AZURE_AI_PROJECT_ENDPOINT="..." \
    AZURE_AI_AGENT_ID="..."

# Deploy
zip -r deploy.zip . -x ".env" "__pycache__/*"
az webapp deployment source config-zip \
  --name your-app \
  --resource-group your-rg \
  --src deploy.zip
```

**Important**: Grant the managed identity access to your AI project in Azure AI Foundry portal.

## 🐛 Troubleshooting

### Authentication Error
```bash
az login
az account set --subscription YOUR_SUBSCRIPTION_ID
```

### Agent Not Found
- Verify `AZURE_AI_PROJECT_ENDPOINT` in `.env`
- Verify `AZURE_AI_AGENT_ID` in `.env`
- Check Azure login has access: `az account show`

### Speech Recognition Failed
- Check browser microphone permissions
- Speak clearly with 1-2 second pause
- Try text chat to isolate issue
- Supported formats: WAV, WebM

### Cosmos DB Connection Failed
- Check `.env` credentials
- Verify firewall allows your IP
- Re-run: `python seed.py`

## 💰 Estimated Costs (Monthly)

- Cosmos DB: $5-10 (400 RU/s)
- Azure AI Foundry: $2-20 (depends on usage)
- Google Speech: **FREE** (up to 60 min/month)
- App Service: $13-55 (B1-B2 tier)

**Total: ~$20-85/month**

## 📊 Conviction Scale

- 0-20%: 🔴 Strongly Resistant
- 21-40%: 🟠 Skeptical  
- 41-60%: 🟡 Warming Up
- 61-80%: 🟢 Somewhat Convinced
- 81-100%: 💚 Ready to Commit!

## 🎓 Persuasion Tips

1. Start with empathy
2. Address objections directly
3. Provide specific benefits
4. Be persistent (4-5 exchanges)
5. Offer concrete solutions

## 📁 Project Structure

```
python-app/
├── app.py              # Flask app (AI Foundry + Google SR)
├── seed.py             # Database seeding
├── requirements.txt    # Dependencies
├── .env.example       # Config template
├── static/
│   └── index.html     # Frontend UI
└── README.md          # This file
```

## ✨ What's Different?

| Feature | Before | Now |
|---------|--------|-----|
| AI | Azure OpenAI API | Azure AI Foundry Agents |
| STT | Azure Speech SDK | Google (free) |
| TTS | Azure Speech SDK | None (text only) |
| Auth | API Keys | DefaultAzureCredential |

## 🎉 Start Persuading!

```bash
python app.py
```

Open **http://localhost:5000** and start practicing your persuasion skills!
