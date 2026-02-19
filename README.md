# Forkast Platform

Prediction-first AI platform for MENA restaurants. Combines demand forecasting, inventory optimization, supplier management, and payment processing into a single platform.

## Architecture

| Service | Port | Technology |
|---------|------|-----------|
| Web UI | 8517 | Streamlit |
| REST API | 8518 | FastAPI |
| Database | - | SQLite (auto-created) |

## Features

- 16-page Streamlit dashboard with horizontal dropdown navigation
- 26 REST API endpoints with Swagger docs
- Demand Forecasting (AI-powered 14-day predictions)
- Inventory Optimization (reorder points, wastage tracking)
- Menu Optimization (food cost %, pricing analysis)
- Labor Scheduling (shift management, peak hours)
- Procurement (PO generation, supplier selection)
- Payment Gateway (Stripe integration with fee model)
- Loyalty Program (5-tier system: Standard / Bronze / Silver / Gold / Platinum)
- Multi-currency support (AED, USD, KWD)

---

## Option A: Deploy to DigitalOcean Droplet

### Step 1 - Create a Droplet

1. Go to https://cloud.digitalocean.com
2. Click **Create** > **Droplets**
3. Choose:
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic, 2 GB RAM / 1 CPU ($12/mo) or higher
   - **Region**: Pick the closest to your users (e.g. Singapore, Frankfurt, or London for MENA)
   - **Authentication**: SSH Key (recommended) or Password
4. Click **Create Droplet**
5. Copy the **IP address** shown (e.g. `164.92.xxx.xxx`)

### Step 2 - Connect to the Droplet

```bash
ssh root@YOUR_DROPLET_IP
```

### Step 3 - Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Verify installation
docker --version
docker compose version
```

### Step 4 - Upload the Project

**Option A - From GitHub (if you pushed the repo):**
```bash
git clone https://github.com/YOUR_USERNAME/forkast-platform.git
cd forkast-platform
```

**Option B - Direct upload from your machine (no GitHub):**
```bash
# On your LOCAL machine (not the droplet), run:
scp -r C:\Users\Administrator\forkast_platform root@YOUR_DROPLET_IP:/root/forkast_platform

# Then on the droplet:
cd /root/forkast_platform
```

### Step 5 - Configure Environment (Optional)

```bash
cp .env.example .env
nano .env
```

Edit the values if needed:
```
FORKAST_ADMIN_API_KEY=your-secure-key-here
FORKAST_STRIPE_SECRET_KEY=sk_live_xxx
FORKAST_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
FORKAST_STRIPE_WEBHOOK_SECRET=whsec_xxx
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

### Step 6 - Build and Start

```bash
docker compose up --build -d
```

This will:
- Build a Docker image with Python 3.12 and all dependencies
- Start both Streamlit (port 8517) and FastAPI (port 8518)
- Auto-create the SQLite database with demo data
- Run in the background (`-d` flag)

Wait about 30 seconds for the build to finish.

### Step 7 - Verify

```bash
# Check container is running
docker ps

# Check logs
docker logs forkast-platform

# Test API health
curl http://localhost:8518/api/v1/health
```

### Step 8 - Open Firewall Ports

```bash
ufw allow 8517/tcp
ufw allow 8518/tcp
```

### Step 9 - Access the Platform

Open in your browser:
- **Platform UI**: `http://YOUR_DROPLET_IP:8517`
- **API Swagger Docs**: `http://YOUR_DROPLET_IP:8518/docs`

### Droplet Management Commands

```bash
# Stop the platform
docker compose down

# Restart the platform
docker compose restart

# Rebuild after code changes
docker compose up --build -d

# View live logs
docker logs -f forkast-platform

# Check container health
docker inspect --format='{{.State.Health.Status}}' forkast-platform
```

---

## Option B: Deploy via GitHub

### Step 1 - Push Code to GitHub

On your local machine:

```bash
cd C:\Users\Administrator\forkast_platform

# Login to GitHub CLI
# Download gh CLI from: https://cli.github.com
gh auth login
# Select: GitHub.com > HTTPS > Login with browser

# Create repo and push
gh repo create forkast-platform --public --push --source=.
```

Your code is now at `https://github.com/YOUR_USERNAME/forkast-platform`

### Step 2 - Automatic Docker Image Build (GitHub Actions)

The repo includes a GitHub Actions workflow at `.github/workflows/docker-build.yml`.

**Enable it:**
1. Go to your repo on GitHub
2. Click **Settings** > **Actions** > **General**
3. Under "Workflow permissions", select **Read and write permissions**
4. Click **Save**

**Trigger the build:**
1. Go to **Actions** tab in your repo
2. Click **Build & Push Docker Image** on the left
3. Click **Run workflow** > **Run workflow**

This builds the image and pushes it to GitHub Container Registry (`ghcr.io`).

### Step 3 - Make the Package Public (Optional)

1. Go to your GitHub profile
2. Click **Packages** tab
3. Click on `forkast-platform`
4. Click **Package settings** (gear icon)
5. Scroll to **Danger Zone** > Change visibility to **Public**

### Step 4 - Deploy on Any Server

SSH into any server (DigitalOcean, AWS, etc.) with Docker installed:

```bash
# Pull the image
docker pull ghcr.io/YOUR_USERNAME/forkast-platform:latest

# Run it
docker run -d \
  --name forkast-platform \
  -p 8517:8517 \
  -p 8518:8518 \
  -e FORKAST_ADMIN_API_KEY=your-secure-key \
  ghcr.io/YOUR_USERNAME/forkast-platform:latest
```

### Step 5 - Access the Platform

- **Platform UI**: `http://YOUR_SERVER_IP:8517`
- **API Swagger Docs**: `http://YOUR_SERVER_IP:8518/docs`

### Share the Link

Once deployed, share the access link with your team:
```
http://YOUR_SERVER_IP:8517
```

---

## Option C: Run Locally (No Docker)

```bash
cd C:\Users\Administrator\forkast_platform

# Install dependencies
pip install -r requirements.txt

# Start both services
bash start.sh
```

Or start each service separately:
```bash
# Terminal 1 - FastAPI
python -m uvicorn api.main:app --host 0.0.0.0 --port 8518

# Terminal 2 - Streamlit
python -m streamlit run web/app.py --server.port 8517 --server.headless true
```

Access at `http://localhost:8517`

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FORKAST_ADMIN_API_KEY` | `fk-admin-dev-key-change-me` | Admin API key for /docs |
| `FORKAST_STRIPE_SECRET_KEY` | *(empty)* | Stripe secret key |
| `FORKAST_STRIPE_PUBLISHABLE_KEY` | *(empty)* | Stripe publishable key |
| `FORKAST_STRIPE_WEBHOOK_SECRET` | *(empty)* | Stripe webhook secret |
| `FORKAST_DEBUG` | `false` | Enable debug/reload mode |

---

## Project Structure

```
forkast_platform/
├── api/                    # FastAPI REST API
│   ├── main.py             # API entry point
│   ├── config.py           # Settings (env vars)
│   ├── database.py         # SQLAlchemy setup
│   ├── auth.py             # API key authentication
│   ├── models/
│   │   ├── db_models.py    # Database ORM models
│   │   └── schemas.py      # Pydantic schemas
│   ├── routers/
│   │   ├── health.py       # Health check endpoints
│   │   ├── pos.py          # POS integration endpoints
│   │   ├── payments.py     # Payment gateway endpoints
│   │   └── loyalty.py      # Loyalty program endpoints
│   └── services/
│       ├── data_service.py     # DB operations
│       ├── stripe_service.py   # Stripe SDK wrapper
│       └── loyalty_service.py  # Loyalty tier logic
├── web/                    # Streamlit Web UI
│   ├── app.py              # Main app (navigation, routing)
│   ├── assets/images.py    # SVG graphics
│   ├── utils/currency.py   # Multi-currency helpers
│   └── pages/              # 16 page modules
├── models/core.py          # Core data models
├── forecasting/            # Demand forecast engine
├── inventory/              # Inventory optimizer
├── data/                   # Demo data generator
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker orchestration
├── start.sh                # Startup script
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
└── .github/workflows/      # CI/CD pipeline
```

## API Documentation

Once running, visit `http://localhost:8518/docs` for interactive Swagger documentation covering all 26 endpoints.
