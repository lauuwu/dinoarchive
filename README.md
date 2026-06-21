# 🦕 DinoArchive

A full-stack dinosaur encyclopedia built as a hands-on DevOps learning project — covering backend API design, containerization, and Kubernetes deployment from the ground up.

## About

DinoArchive started as a way to learn DevOps and Kubernetes by building something real instead of following disconnected tutorials. It grew into a small but complete platform: a FastAPI backend, a PostgreSQL database, a vanilla JS frontend, and a full Kubernetes deployment (manifests + Helm chart) running locally on Minikube.

The project intentionally avoids frontend frameworks and ORM magic shortcuts — the goal was to understand what's actually happening at each layer (HTTP, SQL, containers, orchestration) rather than to ship the fastest possible app.

## Features

- **Dinosaur encyclopedia** — 30 species with period, diet, length, description, and a fun fact, each with a custom hand-drawn SVG illustration
- **Authentication** — JWT-based register/login, bcrypt password hashing, persisted sessions
- **Welcome emails** — sent via SMTP on signup (Gmail), fails gracefully if not configured
- **Quiz & leaderboard** — multiple-choice questions per species, points awarded for correct answers, top-10 leaderboard
- **Blog** — admin-only publishing (role-based access control), public reading
- **Image gallery** — admin file uploads with validation, served from a Kubernetes PersistentVolume so uploads survive pod restarts
- **User profile** — score, join date, account info

## Tech stack

| Layer | Tools |
|---|---|
| Backend | FastAPI, SQLAlchemy, Pydantic, python-jose (JWT), passlib + bcrypt |
| Database | PostgreSQL |
| Frontend | Vanilla HTML/CSS/JS (no framework, by design) |
| Containers | Docker |
| Orchestration | Kubernetes (Minikube), Helm |
| Networking | NGINX Ingress Controller |
| Storage | PersistentVolumeClaims (Postgres data + uploaded images) |

## Architecture

```
                         ┌─────────────────┐
  Browser  ── Ingress ──▶│  backend-service │── ClusterIP ──▶  backend Pod (FastAPI)
 (frontend                └─────────────────┘                        │
  static file)                                                       │
                                                                       ▼
                                                            ┌───────────────────┐
                                                            │  postgres-service  │
                                                            └───────────────────┘
                                                                       │
                                                                       ▼
                                                              PersistentVolumeClaim
                                                               (postgres data)

  backend Pod also mounts a second PersistentVolumeClaim for
  user-uploaded gallery images (/app/uploads), independent of
  the Postgres volume.
```

Everything runs inside a single Kubernetes namespace (`dinoarchive`), with config split across a `ConfigMap` (non-sensitive values) and a `Secret` (passwords, JWT signing key, SMTP credentials).

## Project structure

```
dinoarchive/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app, router registration, static file mount
│   │   ├── models.py          # SQLAlchemy models (User, Dinosaur, QuizQuestion, BlogPost, GalleryImage)
│   │   ├── schemas.py         # Pydantic request/response schemas
│   │   ├── database.py        # DB engine/session setup
│   │   ├── auth_utils.py      # JWT creation, password hashing, role-based dependencies
│   │   ├── email_utils.py     # SMTP welcome email (fails silently, never blocks signup)
│   │   └── routers/           # auth, dinos, quiz, blog, gallery
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   └── index.html             # Single-file frontend (HTML/CSS/JS)
├── k8s/                       # Raw Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── ingress.yaml
│   ├── backend/                (Deployment, Service, gallery PVC)
│   └── postgres/                (Deployment, Service, PVC)
├── dinoarchive-chart/         # Equivalent Helm chart (parameterized via values.yaml)
├── docker-compose.yml         # Local non-Kubernetes alternative
├── seed_dinos.sh               # Loads the first 10 species
├── seed_dinos_batch2.sh        # Loads 20 more species
└── seed_quiz.py                 # Loads quiz questions, matched by dinosaur name
```

## Getting started

### Option 1 — Kubernetes (Minikube + Helm)

```bash
minikube start
minikube addons enable ingress

helm install dinoarchive ./dinoarchive-chart

eval $(minikube docker-env)
docker build -t lauuwu/dinoarchive-backend:latest ./backend

kubectl port-forward svc/ingress-nginx-controller 8080:80 -n ingress-nginx
```

Add `127.0.0.1 dinoarchive.local` to your hosts file, then open `frontend/index.html` in a browser.

### Option 2 — Raw manifests instead of Helm

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/postgres/
kubectl apply -f k8s/backend/
kubectl apply -f k8s/ingress.yaml
```

### Option 3 — docker-compose (no Kubernetes)

```bash
docker-compose up --build
```

### Seeding data

```bash
bash seed_dinos.sh
bash seed_dinos_batch2.sh
python3 seed_quiz.py
```

## Environment variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing secret |
| `SMTP_HOST` / `SMTP_PORT` | SMTP server for welcome emails (defaults to Gmail) |
| `SMTP_USER` / `SMTP_PASSWORD` | SMTP credentials (Gmail app password, not your real password) |
| `UPLOAD_DIR` | Path where gallery images are stored (mounted PVC in Kubernetes) |

All secrets are injected via a Kubernetes `Secret`, never hardcoded.

## API overview

| Method & path | Description | Auth |
|---|---|---|
| `POST /auth/register` | Create account, sends welcome email | — |
| `POST /auth/login` | Returns JWT | — |
| `GET /auth/me` | Current user info | required |
| `GET /dinos/` | List all species | — |
| `GET /quiz/dino/{id}` | Quiz questions for a species | — |
| `POST /quiz/answer` | Submit an answer, awards points | required |
| `GET /quiz/leaderboard` | Top 10 scores | — |
| `GET /blog/` | List blog posts | — |
| `POST /blog/` | Create post | admin only |
| `GET /gallery/` | List images | — |
| `POST /gallery/` | Upload image (multipart) | admin only |

## Roadmap

- [ ] E-commerce catalog section
- [ ] Cloud deployment (currently local-only via Minikube)
- [ ] CI/CD pipeline (GitHub Actions → Docker Hub → cluster)
- [ ] Admin panel for promoting users (currently done via direct SQL)

## Author

Built by [lauuwu](https://github.com/lauuwu) — self-taught, learning DevOps and Kubernetes from the ground up, one broken pod at a time.
