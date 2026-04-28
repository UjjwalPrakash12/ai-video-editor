# AI Video Editor (Unified Repo)

This folder combines your old split repos into one project:

- `frontend/` - Browser UI (upload + chat commands)
- `backend/` - Flask API and processing pipeline

## Quick start

### Option A: One command start

```bash
cd ai-video-editor
chmod +x start.sh
./start.sh
```

This starts:
- Backend: `http://127.0.0.1:5001`
- Frontend: `http://127.0.0.1:8080`

### Option B: Manual backend start

```bash
cd ai-video-editor/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Backend runs at `http://localhost:5001`.

### Frontend

Use a static server:

```bash
cd ai-video-editor/frontend
python3 -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080`.

## Docker

```bash
cd ai-video-editor
docker compose up --build
```

Then open:
- Frontend: `http://127.0.0.1:8080`
- Backend API: `http://127.0.0.1:5001/api/health`

If backend is running, UI will call:
- `POST /api/upload`
- `POST /api/command`

## Notes

- Works in mock mode if `moviepy` or `whisper` is unavailable.
- Uploaded videos are stored in `backend/uploads/`.
- Render outputs are stored in `backend/outputs/`.
