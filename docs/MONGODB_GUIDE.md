# 🍃 MongoDB Integration Guide

This guide explains how to connect your **Task Review AI** to a MongoDB database for persistent storage. Without this, all data is lost when the Render service restarts.

## 1. Get a MongoDB Connection String
The easiest way is to use **MongoDB Atlas** (Free Tier):
1. Sign up/Log in at [mongodb.com](https://www.mongodb.com/cloud/atlas).
2. Create a new Cluster (Shared/Free).
3. Under **Network Access**, allow access from anywhere (`0.0.0.0/0`) for the demo, or specifically add Render's IP if you have it.
4. Under **Database Access**, create a user with a password.
5. Click **Connect** -> **Drivers** -> **Python**.
6. Copy the Connection String (URI). It looks like:
   `mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0`

---

## 2. Configure Render
1. Go to your **Render Dashboard**.
2. Select your `task-review-backend` service.
3. Go to **Environment**.
4. Add a new Environment Variable:
   - **Key**: `MONGODB_URI`
   - **Value**: Paste your connection string from Step 1.
5. Click **Save Changes**.

---

## 3. Deployment Details
- **Automatic Fallback**: If the `MONGODB_URI` is not provided, the system will automatically fall back to **In-Memory Storage**. You will see a warning in the logs: `MONGODB_URI not found. System will fallback to in-memory storage.`
- **Library Used**: We use `motor` for asynchronous MongoDB operations to ensure the API stays fast.
- **Persistence**: Once connected, task submissions are saved to the `tasks` collection in your default database. When you request a review later (even after a restart), the system will fetch the task from MongoDB.

---

## 4. Verification
1. Submit a task via the Streamlit UI.
2. Check your MongoDB Atlas "Browse Collections" tab. You should see a data entry in the `tasks` collection.
3. Trigger a manual deploy in Render (which restarts the service).
4. Try to view the previous analysis or run it again—it should still work!
