# Lumio

Lumio is a multimodal video intelligence app for ingesting recordings, indexing transcript plus visual context, and exploring answers inside an AI workspace with evidence and playback.

## Repo Layout

This repository currently contains both apps:

- `backend/` - FastAPI ingestion, indexing, search, and workbench APIs
- `frontend/` - Next.js AI workspace, ingest flow, and library UI

## Local Setup

### Backend

```bash
cd backend
copy .env.example .env
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend

```bash
cd frontend
copy .env.example .env.local
npm install
npm run dev
```

Open:

- frontend: [http://127.0.0.1:3000](http://127.0.0.1:3000)
- backend docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Environment Variables

Backend:

```env
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=https://your-qdrant-cluster-url
QDRANT_API_KEY=your_qdrant_api_key
```

Frontend:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Splitting Into Separate Repositories

If you want separate repos for deployment, the clean split is:

- `lumio-backend`
- `lumio-frontend`

Recommended contents for the backend repo:

- everything inside `backend/`

Recommended contents for the frontend repo:

- everything inside `frontend/`

One way to split from this monorepo is with `git subtree`:

```bash
git subtree split --prefix=backend -b split/backend
git subtree split --prefix=frontend -b split/frontend
```

Then push each branch to its own GitHub repository.

## Safety Checklist

Already excluded from git:

- `backend/.env`
- `backend/uploads/`
- `backend/frames/`
- `backend/metadata/`
- `backend/qdrant_data/`
- `frontend/.env.local`
- `frontend/.next/`
- log files
- local video files

Before pushing split repos, also double-check:

- no real API keys are in committed source
- no generated logs are staged
- no local media or cached frame directories are staged

## Documentation

- backend setup and deployment: `backend/README.md`
- frontend setup and deployment: `frontend/README.md`
