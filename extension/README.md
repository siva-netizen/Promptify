# Promptify Extension (Product B)

This directory contains the Chrome Extension and Cloud Backend for Promptify.

## Structure

- **backend/**: FastAPI service that runs the Promptify core logic. designed for cloud deployment (Railway, Vercel, etc.).
- **client/**: The Chrome Extension source code.

## Setup & Running Locally

### 1. Start the Backend API
You need to run the backend service so the extension can talk to it.

```bash
# From this directory
.\run_server.bat
```
*Or manually:*
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
The server will start at `http://localhost:8000`.

### 2. Install the Extension
1. Open Chrome and go to `chrome://extensions`.
2. Enable **Developer Mode** (top right).
3. Click **Load unpacked**.
4. Select the `extension/client` folder.

### 3. Usage
1. Go to **ChatGPT** or **Claude**.
2. Look for the ✨ **Refine** button near the input box.
3. Type a simple prompt (e.g., "build a snake game").
4. Click **Refine**.
5. A modal will appear with the refined professional spec.
6. Click **Confirm** to replace your input.

## Deployment
To deploy the backend to the cloud:
1. Ensure `cli/src` is included or installed as a package.
2. Deploy the `backend/` folder as a Python web service.
3. Update the Extension's API URL in the Popup Settings.
