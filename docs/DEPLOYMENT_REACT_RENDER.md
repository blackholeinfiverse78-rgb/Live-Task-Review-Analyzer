# 🚀 Deploying React Frontend to Render

This guide explains how to deploy the **Task Review AI** system with the new React frontend.

## Prerequisites
1. A [GitHub](https://github.com) account with the project repository pushed.
2. A [Render](https://render.com) account.

---

## Method 1: Blueprint Deployment (Recommended)

1. Log in to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** and select **Blueprint**.
3. Connect your GitHub repository.
4. Render will detect the `render.yaml` file.
5. Click **Apply**.
6. Render will automatically create:
   - `task-review-backend` (Web Service - FastAPI)
   - `task-review-frontend-react` (Static Site - React)
7. The frontend will automatically use the backend's public URL.

---

## Method 2: Manual Deployment

### Step 1: Deploy the Backend (FastAPI)
1. Go to **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure:
   - **Name**: `task-review-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `ALLOWED_ORIGINS`: `["*"]`
5. Click **Deploy Web Service**.
6. **Copy the backend URL** (e.g., `https://task-review-backend-xxxx.onrender.com`).

### Step 2: Deploy the Frontend (React)
1. Go to **New +** -> **Static Site**.
2. Connect the same GitHub repository.
3. Configure:
   - **Name**: `task-review-frontend-react`
   - **Build Command**: `cd frontend-react && npm install && npm run build`
   - **Publish Directory**: `frontend-react/build`
4. Add Environment Variables:
   - `REACT_APP_BACKEND_URL`: Paste your backend URL + `/api/v1/task`
     - Example: `https://task-review-backend-xxxx.onrender.com/api/v1/task`
5. Click **Create Static Site**.

---

## Local Development

### Backend
```bash
# From project root
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend-react
npm install
npm start
```

The React app will run on `http://localhost:3000` and proxy requests to `http://localhost:8000`.

---

## Important Notes

### 1. Static Site vs Web Service
The React frontend is deployed as a **Static Site** on Render, which is:
- Free forever (no spin-down)
- Served via CDN (faster)
- No server-side code execution

### 2. Environment Variables
React environment variables must be prefixed with `REACT_APP_` and are **baked into the build** at build time. If you change the backend URL, you must **redeploy** the frontend.

### 3. CORS Configuration
Ensure your backend's `ALLOWED_ORIGINS` includes `*` or your specific frontend URL.

---

## Troubleshooting

### Build Fails
- Ensure Node.js version is compatible (Render uses Node 14+ by default)
- Check build logs for npm errors
- Verify `package.json` is valid

### Backend Connection Issues
1. Check the backend URL in the frontend environment variables
2. Ensure it includes `/api/v1/task` at the end
3. Verify CORS is properly configured on the backend
4. Check browser console for specific error messages

### Static Site Not Updating
- Clear your browser cache
- Trigger a manual redeploy in Render Dashboard
- Verify the build command completed successfully

---

## Features of React Frontend

✨ **Modern Design**
- Beautiful gradient backgrounds
- Smooth animations and transitions
- Glassmorphism effects
- Responsive mobile-first design

🚀 **Enhanced UX**
- Real-time backend status indicator
- Loading states with spinners
- Error handling with user-friendly messages
- Interactive progress bars

📊 **Same Functionality**
- All demo scenarios from Streamlit version
- Complete task submission and review flow
- Detailed analysis and metrics display
- Next task recommendations
