# McLaren Pit Wall — Backend

FastAPI service powering the dual-mode AI Race Engineer.

## Files
- `main.py` — Core API: routing, server setup, and logic/personas for both
  Paddock Mode (normal AI) and Race Engineer Mode (aggressive F1 tone).
- `app1.py` — Backup: Weather & Environmental Conditions agent (standalone).
- `app2.py` — Backup: Race Strategy & Telemetry agent (standalone).

## Run

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key
export ANTHROPIC_BASE_URL=your-base-url   # optional
uvicorn main:app --reload --port 8000
```

If `ANTHROPIC_API_KEY` is not set, the service returns deterministic mock
replies so the frontend still works end-to-end.

## Endpoints
- `GET  /health` — `{ "status": "ok" }`
- `GET  /tracks` — list of available circuits
- `POST /chat`   — `{ mode, track_id, message, history }` → `{ reply, tokens_used, latency_ms }`
