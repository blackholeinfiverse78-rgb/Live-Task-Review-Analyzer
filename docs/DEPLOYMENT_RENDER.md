# 🚀 Deploying to Render: Step-by-Step Guide

This guide explains how to deploy the **Task Review AI** system (FastAPI backend + Streamlit frontend) to [Render](https://render.com).

## Prerequisites
1. A [GitHub](https://github.com) account with the project repository pushed.
2. A [Render](https://render.com) account.

---

## Method 1: Blueprint Deployment (Recommended)
We have included a `render.yaml` file in the root directory. This allows you to deploy both services automatically.

1. Log in to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** and select **Blueprint**.
3. Connect your GitHub repository.
4. Render will detect the `render.yaml` file. 
5. Click **Apply**.
6. Render will automatically create:
   - `task-review-backend` (Web Service)
   - `task-review-frontend` (Web Service)
7. Render will automatically link the frontend to the backend using the internal URL.

---

## Method 2: Manual Deployment

If you prefer to set things up manually or want more control, follow these steps:

### Step 1: Deploy the Backend (FastAPI)
1. Go to **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure the following:
   - **Name**: `task-review-backend`
   - **Environment**: `Python 3` (or `Python`)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `ALLOWED_ORIGINS`: `["*"]` (or specific frontend URL once deployed)
5. Click **Deploy Web Service**.
6. **Note the URL**: After deployment, copy the backend URL (e.g., `https://task-review-backend.onrender.com`).

### Step 2: Deploy the Frontend (Streamlit)
1. Go to **New +** -> **Web Service**.
2. Connect the same GitHub repository.
3. Configure the following:
   - **Name**: `task-review-frontend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run frontend/streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
4. Add Environment Variables:
   - `BACKEND_URL`: Paste the backend URL you copied earlier.
     - Example: `https://task-review-backend.onrender.com`
     - (The app will automatically append `/api/v1/task` for you).
5. Click **Deploy Web Service**.

---

## Important Considerations

### 1. Cold Starts (Free Tier)
If you are using Render’s **Free Tier**, the services will "spin down" after 15 minutes of inactivity. The first request after a spin-down can take 30-60 seconds to respond as the instance wakes up.

### 2. In-Memory Storage
This application uses **In-Memory Storage** (`LimitedStorage`) for the demo. 
- **Data Persistence**: Data will be cleared whenever the service restarts (every deploy or daily restart).
- **Scale**: If you scale to multiple instances, data will not be shared between them unless you implement a database (e.g., MongoDB, PostgreSQL).

### 3. Monitoring Health
- Backend Health: `https://your-backend-url.onrender.com/health`
- Frontend Sidebar: The Streamlit app sidebar will show "Backend Online" if the connection is successful.

---

## Troubleshooting

### Build Fails
- Ensure `requirements.txt` is present and doesn't contain platform-specific packages (like `pywin32` which is for Windows only).
- Check the build logs in Render Dashboard for specific error messages.

### Streamlit Port Error
- Render requires services to listen on `$PORT`. Ensure the start command uses `--server.port $PORT`.

### Backend Offline / Connection Error
**This is the most common issue on Render's Free Tier.**

**Symptoms**: Frontend shows "Backend Offline" with `ConnectionError` in the sidebar.

**Root Cause**: Internal networking (`task-review-backend` hostname) is unreliable on Render's Free Tier.

**Solution**:
1. Go to your Render Dashboard
2. Click on **`task-review-backend`** service
3. **Copy the public URL** (e.g., `https://task-review-backend-xxxx.onrender.com`)
4. Click on **`task-review-frontend`** service
5. Go to **Environment** tab
6. Find `BACKEND_URL` and click **Edit**
7. Replace the value with your backend's **public HTTPS URL**
8. Click **Save Changes**
9. Wait for the frontend to redeploy (~2-3 minutes)

### CORS Errors
- If the frontend cannot talk to the backend, check the `ALLOWED_ORIGINS` variable in the backend settings.
- For development/demo purposes, `["*"]` allows all origins. For production, specify your frontend URL.
