# Mobile Shopping Chat Agent

AI-powered shopping assistant for mobile phones in the Indian market.

## Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API key

### Backend Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp env.example .env
# Add your GOOGLE_API_KEY to .env

cd backend
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

## Tech Stack

**Backend:** FastAPI, LangChain, Google Gemini 2.5 Flash, Pydantic

**Frontend:** React, Vite, Tailwind CSS

**Data:** JSON catalog with 40 phones (₹10k-₹50k range)

## Architecture

```
backend/
├── agents/        # LangChain agent and tools
├── api/           # FastAPI routes
├── dao/           # Data access layer
├── dto/           # Pydantic models
├── services/      # Business logic and safety
├── data/          # Phone catalog
└── main.py

frontend/
├── src/
│   ├── components/
│   ├── services/
│   └── App.jsx
└── package.json
```

## Features

- Natural language search ("Best camera phone under ₹30k?")
- Phone comparisons ("Compare Pixel 8a vs OnePlus 12R")
- Technical explanations ("Explain OIS vs EIS")
- Adversarial prompt protection
- Conversational context

## Prompt Engineering

System prompt enforces:
- Mobile phone shopping only
- Tool-based data access (no hallucination)
- Neutral, factual responses
- Refusal of adversarial requests

Safety layer includes:
- Input validation and sanitization
- Adversarial pattern detection
- Toxic content filtering
- Off-topic query rejection

## 🌐 Live Demo

- **Frontend**: [Will be added after deployment]
- **Backend API**: [Will be added after deployment]
- **API Docs**: [Backend URL]/docs

## Deployment

### Backend (Render.com)
1. Create new Web Service on Render
2. Connect GitHub repo
3. Build: `pip install -r requirements.txt`
4. Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add env var: `GOOGLE_API_KEY`

### Frontend (Vercel)
1. Create new project on Vercel
2. Root directory: `frontend`
3. Add env var: `VITE_API_URL` (your Render backend URL)

## Known Limitations

- Static phone catalog (not real-time)
- 40 phones (representative sample)
- In-memory sessions
- Indian market only

## API Endpoints

- `POST /api/chat` - Chat with agent
- `GET /api/phones` - List all phones
- `GET /api/phones/{id}` - Phone details
- `GET /api/health` - Health check

Docs: `http://localhost:8000/docs`
