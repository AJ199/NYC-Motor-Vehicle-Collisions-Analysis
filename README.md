# TokenMetrics — Market Indices & Crypto Overview

A full-stack web application that displays real-time market indices and cryptocurrency prices with a 30-day trend chart.  
It uses React + Vite for the frontend and Node.js + Express for the backend.  
All data is fetched from the Financial Modeling Prep (FMP) API, with a built-in server-side caching layer that improves performance, prevents redundant API calls, and keeps the app resilient during outages.

---

## Environment Setup

### Overview

This project has two main layers:

1. **Backend (Express server)** — Handles API requests, caching, rate-limiting, and fallback data logic.  
2. **Frontend (React app)** — Displays live index cards and charts using Chart.js.

Both services run concurrently with a single command.

---

### Step-by-Step Setup

#### Clone and Install Dependencies

```bash
git clone https://github.com/YOUR_USERNAME/tokenmetrics-app.git
cd tokenmetrics-app
npm install
npm run dev
open http://localhost:5173

## About the Demo API Key

The demo API key from Financial Modeling Prep is globally shared and ideal for testing.  
However, it comes with limited daily usage and may occasionally cause HTTP 403 or 429 errors if the limit is reached.

---

## Caching Strategy

### Purpose

Financial APIs often have strict rate limits — for example, the free FMP API allows only 20 requests per minute.  
If every frontend refresh triggered new API calls, the app would quickly exceed its quota.

To solve this, the backend implements a **Time-To-Live (TTL)** based caching system.

---

### How It Works

When an endpoint such as `/api/indices` or `/api/history/:symbol` is requested:

1. The server checks if a cached entry exists and whether it’s still valid.  
2. If valid → returns data directly from memory.  
3. If expired or missing → makes a new API request, stores the response in cache, and returns it.  
4. If the vendor API fails (403/429/500), the server gracefully serves the last cached snapshot or fallback mock data.

