# Deployment Guide for RAIF-Edu

This project is fully configured for production deployment across all major cloud providers and free hosting platforms.

---

## 🌟 Option 1: Free 1-Click Cloud Deployment (Render.com) — *Recommended*

**Render** offers completely free web service hosting for Python web applications.

### Steps:
1. **Push your code to GitHub**:
   Create a new GitHub repository (e.g., `raif-edu-framework`) and run:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/raif-edu-framework.git
   git branch -M main
   git push -u origin main
   ```
2. **Deploy on Render**:
   * Go to [dashboard.render.com](https://dashboard.render.com/) (Sign in with GitHub).
   * Click **New +** $\rightarrow$ **Web Service**.
   * Select your `raif-edu-framework` repository.
   * Render automatically detects:
     * **Environment**: `Python 3`
     * **Build Command**: `pip install -r requirements.txt`
     * **Start Command**: `gunicorn web.app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4` (from [`Procfile`](./Procfile) and [`render.yaml`](./render.yaml))
   * Select the **Free** instance type and click **Create Web Service**.
3. **Your Live Public URL**:
   In ~2 minutes, your project will be live at:
   `https://raif-edu-framework.onrender.com`

---

## 🚀 Option 2: Serverless Deployment on Vercel

The project includes a ready-to-deploy [`vercel.json`](./vercel.json).

### Steps:
1. Open your terminal in the project directory:
   ```bash
   cd C:\Users\HP\.gemini\antigravity\scratch\responsible-ai-edu-framework
   ```
2. Run Vercel CLI (or connect on [vercel.com](https://vercel.com/)):
   ```bash
   npx vercel
   ```
3. Follow the prompts. Vercel will build and assign you a free `*.vercel.app` public domain.

---

## 🤗 Option 3: Hugging Face Spaces (Free AI Cloud Hosting)

Hugging Face Spaces provides free, dedicated 24/7 cloud hosting for AI and Responsible AI research projects.

### Steps:
1. Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2. Set **Space Name** to `responsible-ai-edu-framework`.
3. Choose **Docker** (Blank) or **Gradio/Flask** as the Space SDK.
4. Clone the space repo and push these files, or upload them directly.
5. Hugging Face will automatically build the [`Dockerfile`](./Dockerfile) and host it with an official Hugging Face URL!

---

## 🐳 Option 4: Universal Container Deployment (Docker)

To deploy on any virtual server (AWS EC2, DigitalOcean, Google Cloud Run, Azure App Service):

```bash
# Build the production Docker image
docker build -t raif-edu .

# Run the containerized service
docker run -d -p 5000:5000 --name raif-edu-container raif-edu
```
Access at `http://YOUR_SERVER_IP:5000`.

---

## ⚡ Option 5: Instant Public HTTPS Tunnel (Zero-Setup in 30 Seconds)

If you need a live public HTTPS link right now (e.g. to share on your mobile phone or demo during a viva defense presentation) while the local server is running:

### Using Cloudflare Tunnel (Free & Instant):
Download Cloudflared or run:
```bash
cloudflared tunnel --url http://localhost:5000
```
It gives you an instant, secure public URL (e.g., `https://random-word.trycloudflare.com`) accessible from any device anywhere in the world!

### Using Pinggy (No Installation Required):
In PowerShell or Command Prompt, run:
```bash
ssh -p 443 -R0:localhost:5000 a.pinggy.io
```
It gives you an immediate live public HTTPS link!
