# Deployment Guide: Vercel (Frontend) & Render/Railway (Backend)

This project is configured to use a **split-hosting architecture**:
1. **Frontend on Vercel** (100% Free)
2. **Backend on Render/Railway** (100% Free option, with optional paid persistent storage upgrades)

---

## 🛠️ Step 1: Push your Code to GitHub

Make sure your local workspace is pushed to a remote GitHub repository.
1. Initialize git and commit your files if you haven't already:
   ```bash
   git init
   git add .
   git commit -m "Configure deployment files"
   ```
2. Create a repository on GitHub and push your local commits.

---

## 💾 Step 2: Deploy the Backend (e.g., on Render)

You can run the backend completely for **free** on Render's Free Web Service tier.

### Option A: 100% Free Tier (Ephemeral Storage)
*Cost: $0.00/month. The container goes to sleep after 15 minutes of inactivity. When it wakes up, any uploaded PDFs and the database cache are reset. However, your API keys and configuration settings remain active if set as environment variables.*

1. **Sign up / Log in** to [Render](https://render.com/).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository.
4. Set the following settings:
   - **Language**: `Docker` (Render will automatically detect the `Dockerfile` at the root of the project).
   - **Branch**: `main` (or your active branch).
5. *(Optional)* In the **Environment Variables** section, you can add default/admin API keys if you want to provide them as system fallbacks for all users. If left blank, users will need to enter their own keys in the app's Settings page:
   - `LLM_MODE` = `api` (sets default mode to API instead of local Ollama)
   - `API_PROVIDER` = `openai` (or `gemini` / `anthropic` to set default provider)
   - `OPENAI_API_KEY` = `your-fallback-openai-api-key`
   - `GEMINI_API_KEY` = `your-fallback-gemini-api-key`
   - `ANTHROPIC_API_KEY` = `your-fallback-anthropic-api-key`
   - `EMBEDDING_MODE` = `api`
   - `EMBEDDING_API_KEY` = `your-fallback-embedding-key`
   
   > [!NOTE]
   > This app is fully **BYOK (Bring Your Own Key)** enabled. End-users can enter their own API keys via the **Settings** menu in the UI. These keys are stored securely in their own browser's `localStorage` and sent dynamically with requests, meaning they will not be lost when the free server restarts.
6. Click **Create Web Service**.
7. Once build completes, copy the backend URL (e.g., `https://rei-backend.onrender.com`).

---

### Option B: Paid Tier (Persistent Storage)
*Cost: ~$7/month (Starter tier) + ~$0.25/month for a persistent disk. Uploaded files and database records persist permanently and never reset.*

1. Perform steps 1-4 from Option A.
2. In settings, choose the **Starter** instance type.
3. Scroll down to **Advanced** and click **Add Disk / Persistent Volume**:
   - **Name**: `rei-data`
   - **Mount Path**: `/data`
   - **Size**: `1 GB` (or more)
4. Add the following **Environment Variables** to map storage to the disk:
   - `CONFIG_PATH` = `/data/config.json`
   - `STORAGE_DIR` = `/data/storage`
   - `CHROMA_DIR` = `/data/chroma_db`
   - Add your API keys (e.g., `OPENAI_API_KEY`, `GEMINI_API_KEY`, etc.) as env variables for convenience.
5. Click **Create Web Service** and copy your backend URL when built.

---

## 🌐 Step 3: Configure and Deploy the Frontend (on Vercel)

Now we connect the frontend to our deployed backend URL using Vercel's rewrite rule.

### A. Update the Proxy URL Locally
1. Open the [frontend/vercel.json](file:///c:/Users/hello/OneDrive/Desktop/AI%20vali%20baat%20chit/rei/frontend/vercel.json) file.
2. Replace `https://YOUR_BACKEND_URL` with your actual backend URL copied from Step 2:
   ```json
   {
     "cleanUrls": true,
     "rewrites": [
       {
         "source": "/api/:path*",
         "destination": "https://rei-backend.onrender.com/api/:path*"
       }
     ]
   }
   ```
3. Commit and push the change to GitHub:
   ```bash
   git add frontend/vercel.json
   git commit -m "Update backend proxy destination"
   git push origin main
   ```

### B. Deploy on Vercel
1. Go to [Vercel](https://vercel.com/) and log in.
2. Click **Add New** -> **Project**.
3. Select your GitHub repository.
4. Under **Configure Project**:
   - Set **Root Directory** to `frontend` (click "Edit" and choose the `frontend` folder).
   - Keep all other build settings as default.
5. Click **Deploy**.

🎉 **Your application is now hosted and ready!** The Vercel frontend will proxy all `/api/*` calls directly to your Render backend safely.
