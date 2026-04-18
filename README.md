# Inbox Copilot (SOFTEC 2026 MVP)

Paste a batch of opportunity emails + a student profile → the backend extracts structured fields and a deterministic engine ranks opportunities by **fit + urgency + value**.

## Demo (Frontend)

```bash
cd frontend
npm install
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`). Click **load 7 sample emails** → fill profile → **Analyze**.

## Backend (FastAPI)

This backend requires **Python 3.10+**.

1) Create `backend/.env` from the example:

- Copy `backend/.env.example` → `backend/.env`
- Add **either** your Claude key **or** your Gemini key (or both)
- Optional: set `LLM_PROVIDER=claude` or `LLM_PROVIDER=gemini`

2) Install and run:

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend should be at `http://localhost:8000` (the frontend calls `/analyze`).

## Notes

- If no API key is configured, the backend uses a lightweight local extractor so the demo still works (but with lower accuracy).
- Do **not** commit your real `.env` (only keep `.env.example` in git).

