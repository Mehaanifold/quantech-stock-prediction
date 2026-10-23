# 📈 Quantech: Stock Analytics & Forecasting Dashboard

A lightweight, interactive stock price analytics and illustrative forecasting web application built with **Python**, **Streamlit**, and **Docker**.

Developed for **Agile Assignment No. 1 (Semester V, TE Data Science)** covering:
- **LO2:** Source Code Management using Git and GitHub.
- **LO3:** Automated CI/CD Pipeline using GitHub Actions, Pytest, Container Packaging (GHCR), and Cloud Deployment.

---

## 📌 Project Overview

Quantech provides an intuitive web platform for inspecting historical stock market price series and visualizing short-term mathematical trend projections using deterministic, hardcoded sample datasets.

### ✨ Key Features
- **Hardcoded Historical Dataset:** Pre-configured 50-day daily OHLCV trading data for Indian equities:
  - `RELIANCE` (Reliance Industries Ltd. — Energy & Telecom)
  - `TCS` (Tata Consultancy Services Ltd. — IT)
  - `INFY` (Infosys Ltd. — IT)
  - `HDFCBANK` (HDFC Bank Ltd. — Banking & Finance)
- **Interactive Price Charting:** Dynamic multi-layered charts using Altair with tooltips, zooming, and panning.
- **Technical Indicators:** Rolling Simple Moving Averages (**SMA-7** and **SMA-14**) to track momentum.
- **Mathematical Forecasting Model:** Ordinary Least Squares (**OLS**) linear trend projection ($y = mx + c$) with residual standard error bands for customizable forecast horizons (3 to 14 days).
- **Automated Testing Suite:** 14 automated unit and integration tests with `pytest`.
- **Automated CI/CD Pipeline:** Multi-stage GitHub Actions workflow building, testing, linting, packaging into Docker, and publishing to GitHub Container Registry (GHCR).
- **Educational Disclaimer:** Clear notice explaining that predictions are illustrative for academic demonstration and not financial advice.

---

## 🏗️ Architecture & Tech Stack

- **Language:** Python 3.10+ (tested on Python 3.12)
- **Web Framework:** [Streamlit](https://streamlit.io/) (v1.30+)
- **Data & Math:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Visualization:** [Altair](https://altair-viz.github.io/)
- **Testing:** [Pytest](https://pytest.org/), [Pytest-Cov](https://pytest-cov.readthedocs.io/)
- **Containerization:** [Docker](https://www.docker.com/) (Debian-slim base)
- **CI/CD Pipeline:** [GitHub Actions](https://github.com/features/actions)
- **Artifact Registry:** [GitHub Container Registry (GHCR)](https://ghcr.io)
- **Live Deployment Platform:** [Streamlit Community Cloud](https://share.streamlit.io/)

### Project Structure
```text
stock-prediction-app/
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions automated CI/CD pipeline
├── tests/
│   └── test_app.py             # 14 automated unit & integration tests
├── .dockerignore               # Files excluded from container image
├── .gitignore                  # Files excluded from Git tracking
├── Dockerfile                  # Container definition with health check
├── requirements.txt            # Python dependencies (Streamlit, Pytest, Pandas)
├── README.md                   # Complete documentation
├── app.py                      # Main Streamlit web application & UI
├── stock_data.py               # Hardcoded datasets and summary metrics
└── prediction.py               # OLS trend extrapolation and SMA models
```

---

## ⚙️ Local Setup & Installation

### 1. Prerequisites
- Python 3.10 or higher
- Git
- (Optional) Docker Desktop

### 2. Navigate to Repository
```powershell
cd c:\Quantech\stock-prediction-app
```

### 3. Create & Activate Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🧪 Running Automated Tests

Run the complete test suite locally using `pytest`:

```bash
# Run tests with verbose output
python -m pytest -v

# Run tests with execution durations
python -m pytest -v --durations=10
```

### What the test suite verifies:
- `test_module_imports`: Core modules (`stock_data`, `prediction`) import cleanly.
- `test_available_tickers` & `test_stock_metadata`: Datasets, tickers, and metadata integrity.
- `test_stock_data_shape_and_columns`: OHLCV columns present, High $\ge$ Low, positive prices.
- `test_stock_data_invalid_ticker`: Graceful `ValueError` on nonexistent stock symbols.
- `test_compute_moving_averages`: Calculation of 7-day and 14-day rolling moving averages.
- `test_prediction_output_structure_and_shape`: Invariance of output lengths ($N + \text{horizon}$).
- `test_prediction_numerical_invariants`: Error bounds validity ($\text{Upper} \ge \text{Price} \ge \text{Lower}$).
- `test_prediction_known_linear_input`: Verifies OLS math on deterministic line $y = 2x + 10$.
- `test_prediction_empty_or_too_small_dataframe`: Error handling on empty inputs.
- `test_disclaimer_text`: Presence of mandatory academic and regulatory disclaimer.

---

## 🚀 Running the Web Application Locally

Launch the Streamlit web dashboard:
```powershell
python -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🐳 Container Packaging with Docker

### 1. Build the Docker Image
```bash
docker build -t quantech-stock-prediction:latest .
```

### 2. Run the Container
```bash
docker run -d -p 8501:8501 --name quantech-app quantech-stock-prediction:latest
```
Access the application at `http://localhost:8501`.

### 3. Verify Container Health
```bash
curl http://localhost:8501/_stcore/health
```

---

## 🔄 GitHub Actions CI/CD Pipeline

The automated pipeline is defined in [`.github/workflows/ci-cd.yml`](file:///.github/workflows/ci-cd.yml) and triggers automatically on:
- Every **push** to the `main` branch.
- Every **pull request** targeting `main`.

### Pipeline Stages

| Stage | Job Name | Runs On | Description |
|---|---|---|---|
| **1. CI** | `ci-build-and-test` | PR & Push | Sets up Python 3.12, installs dependencies, runs syntax/compilation checks (`py_compile`), executes 14 `pytest` tests, and validates Docker container buildability. |
| **2. CD** | `cd-package-and-publish` | Push to `main` only | Logs into GitHub Container Registry (`ghcr.io`) using `GITHUB_TOKEN`, tags the image with `:latest` and `:sha-<commit>`, and publishes the production image to GHCR. |
| **3. Deploy** | `cd-deploy-trigger` | Push to `main` only | Signals the deployment webhook (e.g. Render / Cloud hook) or triggers continuous deployment on Streamlit Community Cloud. |

### Pulling the Published Container Image from GHCR
Once published by the pipeline:
```bash
docker pull ghcr.io/<YOUR_GITHUB_USERNAME>/quantech-stock-prediction:latest
docker run -d -p 8501:8501 ghcr.io/<YOUR_GITHUB_USERNAME>/quantech-stock-prediction:latest
```

---

## 🌐 Live Application Deployment (Streamlit Community Cloud)

Streamlit Community Cloud offers zero-configuration continuous deployment natively integrated with GitHub:

### Setup Steps:
1. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
2. Click **New app**.
3. Select your repository: `Mehaanifold/quantech-stock-prediction`.
4. Set **Branch**: `main`.
5. Set **Main file path**: `app.py`.
6. Click **Deploy!**

### How Continuous Deployment Works:
Whenever a new commit or feature is merged and pushed to `main`, Streamlit Community Cloud automatically detects the push, pulls the latest code, installs dependencies from `requirements.txt`, and redeploys the live application seamlessly without downtime.

---

## 📸 Screenshots to Capture for Your Practical Journal (Q3)

| # | Screenshot Target | What to Show |
|---|---|---|
| **1** | Terminal — `pytest -v` | All 14 automated tests passing in under 1 second. |
| **2** | Terminal — `docker build` & `docker run` | Container building cleanly and responding to health check on port 8501. |
| **3** | GitHub — **Actions** Tab | Workflow run showing green checkmarks for `ci-build-and-test`, `cd-package-and-publish`, and `cd-deploy-trigger`. |
| **4** | GitHub — **Packages** Page | The published container image on GitHub Container Registry with tags `:latest` and `:sha-xxxxxxx`. |
| **5** | Streamlit Community Cloud | Live running application URL with interactive charts and prediction sliders. |

---

## ⚠️ Academic & Regulatory Disclaimer

> **IMPORTANT NOTICE:**  
> This application is strictly an **educational tool** developed for practical demonstration in **Agile Assignment No. 1 (Semester V, TE Data Science)**. All stock price datasets and linear projections are hardcoded/mathematical approximations and do **not** reflect real-time financial market movements. This is **NOT financial advice**.
