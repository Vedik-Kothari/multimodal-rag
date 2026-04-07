# Lumio

Lumio is an AI video intelligence platform for turning long recordings into searchable, evidence-backed knowledge.

It supports video upload or link ingestion, transcript and frame processing, multimodal retrieval, grounded answers, a dedicated AI workspace, and a browsable video library.

## What We Built

Lumio combines a FastAPI backend and a Next.js frontend into a workflow that goes from raw video to usable knowledge.

Core capabilities:

- Upload local videos or ingest YouTube and direct video links
- Run progressive processing so search becomes available before full enrichment finishes
- Extract transcript, frames, and multimodal chunks for retrieval
- Ask grounded questions with timestamped evidence
- Use structured AI tools like Save Time, Moment Map, Cross-Video Memory, Resources, and Decision Mode
- Open cited evidence in a synced player
- Browse indexed videos in a dedicated library
- Export answers as Markdown, text, JSON, HTML, or PDF/print

## Product Structure

- `backend/`
  FastAPI API for ingestion, processing, search, metadata, and workbench outputs
- `frontend/`
  Next.js app for overview, ingest, workspace, and library experiences

## How It Works

1. A user uploads a file or submits a video URL.
2. The backend downloads or saves the video.
3. Audio is extracted and transcribed.
4. Frames are sampled, deduplicated, and captioned.
5. Transcript and visual context are chunked and embedded.
6. Chunks are indexed in Qdrant.
7. The frontend queries the backend and renders grounded answers, evidence, and player jumps.

## Main Features

### Ingestion

- Local file upload
- YouTube and remote link ingestion
- Live progress tracking
- Progressive indexing status

### Retrieval and AI

- Transcript-first retrieval for faster readiness
- Visual enrichment for better multimodal grounding
- Video-scoped search or library-wide search
- Structured workbench modes for different analysis tasks
- Evidence-backed answers with timestamps and source snippets

### Workspace

- Dedicated AI-first workspace
- Separate answer, evidence, and player views
- Quick tool switching
- Export options for generated answers

### Library

- Indexed video browsing
- Metadata-aware cards
- Video selection for focused analysis
- Current video, single video, or all-video context

## Local Development

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

### Backend

```env
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=https://your-qdrant-cluster-url
QDRANT_API_KEY=your_qdrant_api_key
```

### Frontend

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Deployment

The project can be deployed either as a monorepo or as separate frontend and backend repositories.

Recommended deployment split:

- frontend -> Vercel
- backend -> Railway, Render, Fly.io, or another Python host with `ffmpeg`

Split repos already prepared:

- `lumio-frontend`
- `lumio-backend`

## Separate Repo Notes

Backend docs:
- [backend/README.md](C:\Users\HP\.gemini\antigravity\scratch\multimodal-rag\backend\README.md)

Frontend docs:
- [frontend/README.md](C:\Users\HP\.gemini\antigravity\scratch\multimodal-rag\frontend\README.md)

## Safety

Ignored from git:

- `.env` files
- uploaded videos
- extracted frames
- generated metadata
- local Qdrant data
- logs
- local build artifacts

Before deploying, confirm:

- API keys are present only in environment variables
- no generated media is committed
- frontend points to the correct backend URL

## Useful Commands

From the repo root:

```bash
python -m compileall backend
cd frontend && npm run lint
```

## Tech Stack

- FastAPI
- Uvicorn
- Next.js App Router
- React 19
- Tailwind CSS
- Framer Motion
- Groq
- Qdrant
- Sentence Transformers
- `yt-dlp`
- `ffmpeg`
