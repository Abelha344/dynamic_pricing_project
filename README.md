# Dynamic pricing project

## Goal

Build a small **dynamic pricing** workflow for **mobile phone listings** on the Ethiopian marketplace [Jiji Ethiopia](https://jiji.com.et):

1. **Collect** listing titles and ETB prices from the site (scraper).
2. **Train** a simple machine-learning model that maps **product name text** → **suggested price** (TF-IDF + linear regression).
3. **Serve** predictions over **HTTP** (FastAPI) and use a **React** web UI to try names interactively.

The model is a **rough estimate** based on words in the title; it does not use images, condition, or inflation adjustment (those can be added later).

---

## Technologies

| Area | Stack |
|------|--------|
| Language | Python 3.12+ (recommended) |
| Data | CSV (`pandas`) |
| ML | `scikit-learn` — `TfidfVectorizer` + `LinearRegression` |
| Scraping | `selenium` (headless Chrome), `webdriver-manager`, `BeautifulSoup4`, `pandas` |
| API | `FastAPI`, `uvicorn`, `pydantic` |
| Frontend | `React` 18, `Vite` 6, `@vitejs/plugin-react` |

---

## Project structure

```
dynamic_pricing_project/
├── README.md                 # This file
├── market_data.csv           # Scraped data: product_name, price (ETB)
├── pricing_core.py           # Load CSV, train pipeline, predict (shared logic)
├── price_ai.py               # CLI: train + sample predictions
├── jiji_scraper.py           # Scrape Jiji mobile phones → market_data.csv
├── backend/
│   ├── main.py               # FastAPI app (/health, /predict)
│   └── requirements.txt      # API + ML dependencies
└── frontend/
    ├── package.json
    ├── vite.config.js        # Dev proxy: /api → http://127.0.0.1:8000
    └── src/                  # React app
```

---

## Prerequisites

- **Python 3** with `venv` support.
- **Node.js** and **npm** (for the frontend).
- **Google Chrome** (Chromium) for the scraper — Selenium uses it headlessly.

Always run Python commands from the **project root** (`dynamic_pricing_project`), not from your home directory, so paths like `backend/requirements.txt` resolve correctly.

---

## Setup (Python)

From the project root:

```bash
cd /path/to/dynamic_pricing_project
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

Install dependencies for the **API and training**:

```bash
pip install -r backend/requirements.txt
```

Install **extra** packages needed only for **scraping**:

```bash
pip install selenium webdriver-manager beautifulsoup4
```

(If you use only the API with an existing `market_data.csv`, you can skip the scraper packages.)

---

## Run commands

### 1. Scrape Jiji → refresh `market_data.csv`

From project root, venv activated:

```bash
python jiji_scraper.py
```

Requires network access and Chrome. Output: `market_data.csv` with columns `product_name` and `price`.

---

### 2. CLI — train and print sample predictions

```bash
python price_ai.py
```

Loads `market_data.csv`, trains the pipeline, prints a few example suggestions.

---

### 3. API — FastAPI + Uvicorn

From project root, venv activated:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

- Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health: `GET http://127.0.0.1:8000/health`
- Predict: `POST http://127.0.0.1:8000/predict`  
  JSON body: `{"product_name": "Samsung Galaxy S21 128 GB"}`  
  Response: `{"product_name": "...", "price_etb": 12345.67}`

**Environment variables (optional)**

| Variable | Purpose |
|----------|---------|
| `MARKET_DATA_PATH` | Absolute or relative path to CSV (default: `market_data.csv` next to project root). |
| `CORS_ORIGINS` | Comma-separated allowed browser origins (default: `http://localhost:5173`). Set when the React app is hosted on another URL. |

Example:

```bash
export MARKET_DATA_PATH=/path/to/my_market_data.csv
export CORS_ORIGINS=http://localhost:5173,https://myapp.example.com
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

---

### 4. Frontend — React (Vite)

Open a **second** terminal. The UI does **not** need the Python venv for `npm`.

```bash
cd /path/to/dynamic_pricing_project/frontend
npm install
npm run dev
```

Open the URL Vite prints (usually [http://localhost:5173](http://localhost:5173)).  
In dev mode, the app calls `/api/predict`, and Vite **proxies** that to `http://127.0.0.1:8000/predict`, so keep the API running on port **8000**.

**Production build (static files)**

```bash
cd frontend
npm run build
```

Serve the `frontend/dist` folder with any static host. If the API is on another origin, build with:

```bash
VITE_API_URL=https://your-api.example.com npm run build
```

and set `CORS_ORIGINS` on the API to match your site’s origin.

---

## Quick start (both API and UI)

**Terminal 1 — project root:**

```bash
cd /path/to/dynamic_pricing_project
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — frontend:**

```bash
cd /path/to/dynamic_pricing_project/frontend
npm install
npm run dev
```

---

## Data format

`market_data.csv` must include:

- `product_name` — string (listing title).
- `price` — number (ETB).

After scraping or editing data, restart the API so it reloads and retrains on startup (or use `--reload` during development).

---

## License

Use and modify for your own purposes; no license file is included by default.
