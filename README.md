# 🧠 NeuralSearch — Multimodal AI Video Intelligence

> Upload any video or YouTube URL → Extract frames + audio → Ask questions in any language → Get timestamped AI answers with video playback.

![Tech Stack](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.2-orange?style=for-the-badge)
![Qdrant](https://img.shields.io/badge/Qdrant-Cloud-purple?style=for-the-badge)

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎬 **Video Ingestion** | Upload `.mp4`/`.mkv` locally or paste any YouTube URL |
| 👁️ **Visual AI** | Llama 3.2 Vision analyzes frames in 2×2 grid composites for 60× speed |
| 🔊 **Speech AI** | Whisper Large V3 transcribes audio with accurate timestamps |
| 🌐 **Multilingual** | Works in Hindi, English, and any language Whisper supports |
| 🔍 **Semantic Search** | Qdrant Cloud vector search returns the most relevant moments |
| ⚡ **Fast** | 2-min video processed in ~3-5 seconds (parallel Vision API calls) |
| 📡 **Live Progress** | Real-time progress bar shows exactly what the AI is doing |
| 🗑️ **Zero Storage** | Rolling cache: only the latest video is kept locally |
| ☁️ **Cloud DB** | Qdrant Cloud stores all vector memory |

---

## 🛠️ Tech Stack

```
Frontend     → Next.js 15 · Tailwind CSS · Framer Motion · Space Grotesk
Backend      → FastAPI · Python 3.11 · Uvicorn
AI Vision    → Groq API (llama-3.2-11b-vision-preview)
AI Speech    → Groq API (whisper-large-v3)
AI Chat      → Groq API (llama-3.1-8b-instant)
Embeddings   → sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2) [local/free]
Vector DB    → Qdrant Cloud (free 1 GB tier)
Deployment   → Railway (backend) + Vercel (frontend)
```

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.11+
- Node.js 18+
- A free [Groq API Key](https://console.groq.com)
- A free [Qdrant Cloud](https://cloud.qdrant.io) cluster (URL + API Key)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/multimodal-rag.git
cd multimodal-rag
```

### 2. Set up the Backend
```bash
cd backend

# Create .env file
cp .env.example .env
# Edit .env and fill in your keys (see below)

pip install -r requirements.txt
python main.py
```

Backend starts at `http://localhost:8000`

### 3. Set up the Frontend
```bash
cd frontend

# Create local env
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

npm install
npm run dev
```

Frontend starts at `http://localhost:3000`

---

## 🔑 Environment Variables

### `backend/.env`
```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
QDRANT_URL=https://your-cluster.aws.qdrant.cloud
QDRANT_API_KEY=xxxxxxxxxxxxxxxxxxxx
```

### `frontend/.env.local` (local dev)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Vercel (production)
```env
NEXT_PUBLIC_API_URL=https://your-railway-backend-url.up.railway.app
```

---

## ☁️ Deployment

### Backend → Railway

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub Repo
3. Select the **`backend/`** folder as the root directory
4. Add environment variables: `GROQ_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`
5. Railway auto-detects the `Dockerfile` and deploys with `ffmpeg` included
6. Copy your Railway URL (e.g. `https://your-app.up.railway.app`)

### Frontend → Vercel

1. Go to [vercel.com](https://vercel.com) → New Project → Import from GitHub
2. Set **Root Directory** to `frontend`
3. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL = https://your-app.up.railway.app
   ```
4. Deploy!

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User's Browser                           │
│   Next.js 15 Frontend (Vercel)                                  │
│   ┌────────────────┐   ┌──────────────────────────────────────┐ │
│   │  Upload Panel  │   │      Search Interface                │ │
│   │  File / URL    │   │  Query → Sources → Video Player      │ │
│   └───────┬────────┘   └───────────────┬──────────────────────┘ │
└───────────┼───────────────────────────┼─────────────────────────┘
            │ POST /api/upload[-link]    │ POST /api/search
            ▼                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Railway)                     │
│                                                                 │
│   yt-dlp → ffmpeg → frame extraction → Pillow grid stitch       │
│       ↓                                    ↓                    │
│   Whisper (Groq)              Llama Vision (Groq) x6 parallel   │
│       ↓                                    ↓                    │
│   Audio segments              Frame captions (grid composites)  │
│       └──────────────┬─────────────────────┘                   │
│                      ▼                                          │
│         Temporal chunking (30s windows)                         │
│                      ▼                                          │
│         SentenceTransformer embeddings                          │
│                      ▼                                          │
│         Qdrant Cloud ←──────────── Vector Search               │
│                                              ↓                  │
│                              Llama 3.1-8b RAG answer            │
└─────────────────────────────────────────────────────────────────┘
            ↑
     Cloud DB: Qdrant Cloud (Free 1GB)
```

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/api/upload` | Upload a local video file |
| `POST` | `/api/upload-link` | Process a YouTube/web video URL |
| `GET` | `/api/progress/{video_id}` | Get processing progress (for progress bar) |
| `POST` | `/api/search` | Semantic search + RAG answer |
| `GET` | `/api/video/{video_id}` | Stream the processed video |

---

## 🧪 How The Speed Optimization Works

Instead of calling the Vision AI once per frame (24 calls × 2s sleep = 48s wait), we:

1. **Extract** 1 frame every 5 seconds (e.g. 24 frames for a 2-min video)
2. **Stitch** 4 consecutive frames into a single 2×2 grid image using Pillow
3. **Fire** all ~6 grid API calls **simultaneously** using `asyncio.gather`
4. **Result:** ~3-5 seconds total vision analysis vs. 2+ minutes previously

---

## 📜 License

MIT — Free to use, fork, and deploy.
