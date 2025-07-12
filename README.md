# KodeKloud License Usage Dashboard

This project is a real-time dashboard that tracks the usage of KodeKloud licenses by EPAM team members. It pulls data from Azure Blob Storage, processes it with an Azure Function, and displays the results using a React-based frontend deployed to Azure Static Web Apps.

## 🌐 Architecture Overview

![Architecture Diagram](https://strepamkkeast2.blob.core.windows.net/kodekloud-inputs/ChatGPT%20Image%20Jun%2011%2C%202025%2C%2004_17_31%20PM.png?sp=r&st=2025-06-11T23:04:40Z&se=2026-02-28T07:04:40Z&sv=2024-11-04&sr=b&sig=vRtbhj%2FTFvVQZcj4uPn%2F4P3XlcFhuJ5gR9fUUPRpc7Y%3D)

## 🧩 Components

- **Azure Blob Storage**: Stores input Excel files (`kode_kloud/root/KodeKloud2025Admin.xlsx`, `kode_kloud/root/activity_leaderboard.xlsx`) and output JSON (`kodekloud_data.json`).
- **Azure Function App**: Triggered via HTTP, processes the Excel files and generates a report in Excel and JSON formats.
- **GitHub Actions**:
  - One workflow generates the JSON report by calling the Azure Function.
  - Another workflow builds and deploys the frontend to Azure Static Web Apps.
- **Azure Static Web Apps**:
  - Hosts the frontend.
  - Integrates with Microsoft Entra ID for secure enterprise login.
- **Authentication**: Uses Entra ID (formerly Azure AD) with `staticwebapp.config.json` to restrict access to EPAM users only.

## 🔐 Authentication Flow

Users accessing the site are redirected to login with their EPAM Entra ID account. Once authenticated, they are granted access to the dashboard. Unauthorized users are blocked.

## 🚀 Deployment Steps

### 1. Frontend
- React + Tailwind + Vite
- Deployed to Azure Static Web Apps
- GitHub Actions builds and pushes to production

### 2. Backend (FastAPI)
A new FastAPI backend now lives under `backend` and replaces the Function App for local development.
The frontend expects this service at `http://backend:8000` when running with Docker, or `http://localhost:8000` during local development.

### Legacy Azure Function
- The legacy Azure Function resides in `backend_old`.
- Python Azure Function hosted in Azure App Service
- Publishes using GitHub Actions and a publish profile
- Processes data from Blob Storage and writes output back

### 3. Secrets (in GitHub)
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `TENANT_ID`
- `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`
- `AZURE_STATIC_WEB_APPS_API_TOKEN_DELIGHTFUL_WATER_0AE8BED0F`

## 📊 Features

- Active/Inactive filtering
- Search and sort
- Dark mode
- Export to Excel
- Charts and summaries

## 🧪 Testing Locally

```bash
cd frontend
npm install
npm run dev
```

## 🐍 Running the Backend Locally

The FastAPI service needs access to Azure Blob Storage. Before starting it,
set the `AZURE_STORAGE_CONNECTION_STRING` environment variable with your
connection string from the Azure portal. You can create a `.env` file inside the
`backend` folder or export it directly:

```bash
export AZURE_STORAGE_CONNECTION_STRING="<your connection string>"
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## 🐳 Running the Frontend with Docker

You can also run the dashboard directly from a Docker container. The `frontend` directory
contains a `Dockerfile` that builds the React app and serves it using NGINX.

```bash
docker build -t kodekloud-dashboard-frontend frontend
docker run -p 8080:80 kodekloud-dashboard-frontend
```

Then visit <http://localhost:8080> in your browser to view the app.

## 🔁 Triggering the Report Generation

The FastAPI report endpoint can be called with:
```bash
curl -X POST http://localhost:8000/report
```

## 👤 Maintainer

Luis Alvarez (luis_alvarez1@epam.com)
