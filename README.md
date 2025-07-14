# KodeKloud License Usage Dashboard

This project is a real-time dashboard that tracks the usage of KodeKloud licenses by EPAM team members. It pulls data from Azure Blob Storage, processes it with a FastAPI backend, and displays the results using a React-based frontend deployed to Azure Static Web Apps.

## 🌐 Architecture Overview

![Architecture Diagram](https://strepamkkeast2.blob.core.windows.net/kodekloud-inputs/ChatGPT%20Image%20Jun%2011%2C%202025%2C%2004_17_31%20PM.png?sp=r&st=2025-06-11T23:04:40Z&se=2026-02-28T07:04:40Z&sv=2024-11-04&sr=b&sig=vRtbhj%2FTFvVQZcj4uPn%2F4P3XlcFhuJ5gR9fUUPRpc7Y%3D)

## 🧩 Components

- **Azure Blob Storage**: Stores input Excel files (`kode_kloud/root/KodeKloud2025Admin.xlsx`, `kode_kloud/root/activity_leaderboard.xlsx`) and output JSON (`kodekloud_data.json`).
- **FastAPI Backend**: Triggered via HTTP, processes the Excel files and generates a report in Excel and JSON formats.
- **GitHub Actions**:
  - One workflow generates the JSON report by calling the FastAPI backend.
  - The previous workflow that deployed the frontend has been removed.
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
- The `azure-static-web-apps-delightful-water-0ae8bed0f.yml` workflow has been removed

### 2. Backend (FastAPI)
A FastAPI backend now lives under `backend`. It exposes Swagger API docs at `/docs` and fully replaces the old Azure Function.
The frontend expects this service at `http://backend:8000` when running with Docker, or `http://localhost:8000` during local development.

### 3. Secrets (in GitHub)
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `TENANT_ID`
- `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`

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

> **Note** The NGINX config proxies API requests to `http://backend:8000`. When
> running the frontend container on its own, add a host mapping so that the name
> `backend` resolves to your host machine where the FastAPI service is running:

```bash
docker run -p 8080:80 \
  --add-host backend:host-gateway \
  kodekloud-dashboard-frontend
```

Alternatively you can run both containers together using Docker Compose.
The repository includes a `docker-compose.yml` that builds both services and
connects them on a shared network. Simply run:

```bash
docker compose up
```

Once the containers start, open <http://localhost:8080> in your browser.

If Nginx logs show `no resolver defined to resolve backend`, ensure Docker's
embedded DNS is used by adding `resolver 127.0.0.11;` in `frontend/nginx.conf`
and rebuilding the frontend image.

## 🔁 Triggering the Report Generation

The FastAPI report endpoint can be called with:
```bash
curl -X POST http://localhost:8000/report
```

## 🛠️ Development Guidelines

- Run `pytest` inside the `backend` folder.
- Run `npm run lint` inside the `frontend` folder.

## 🆕 Recent Updates

- Removed the old `backend_old` Azure Function directory.
- Backend endpoints are now asynchronous with improved error handling.
- Added a `settings` module powered by `pydantic-settings` for configuration.
- Introduced unit tests for the report endpoints and helper utilities.
- API docs tag renamed from `report` to `KodeKloud`.
- Added a new simplified React frontend under `frontend` that uses the
  `uui-theme-eduverse_dark` styles and shows report data in a table.
- Added a Dockerfile and `nginx.conf` so the frontend can run via Docker Compose.

## 👤 Maintainer

Luis Alvarez (luis_alvarez1@epam.com)
