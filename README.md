# 📈 Quantech: Stock Analytics & Forecasting Dashboard

A lightweight, interactive stock price analytics and illustrative forecasting web application built with **Python** and **Streamlit**. 

Developed as part of **Agile Assignment No. 1 (Semester V, TE Data Science)** to demonstrate **LO2 (Source Code Management using Git and GitHub)**.

---

## 📌 Project Overview

Quantech provides an intuitive dashboard for inspecting historical stock market price series and visualizing short-term mathematical trend projections using deterministic, hardcoded sample datasets.

### ✨ Key Features
- **Hardcoded Historical Dataset:** Pre-configured 50-day daily OHLCV trading data for prominent Indian equities:
  - `RELIANCE` (Reliance Industries Ltd. — Energy & Telecom)
  - `TCS` (Tata Consultancy Services Ltd. — IT)
  - `INFY` (Infosys Ltd. — IT)
  - `HDFCBANK` (HDFC Bank Ltd. — Banking & Finance)
- **Interactive Price Charting:** Dynamic multi-layered charts using Altair with tooltip inspection, zooming, and panning.
- **Technical Indicators:** Rolling Simple Moving Averages (**SMA-7** and **SMA-14**) to observe short- and medium-term momentum.
- **Mathematical Forecasting Model:** Transparent Ordinary Least Squares (**OLS**) linear trend projection ($y = mx + c$) with residual standard error bands for customizable forecast horizons (3 to 14 days).
- **Data Export:** Instant CSV export capability for offline data analysis.
- **Educational Disclaimer:** Prominent notice highlighting the academic and illustrative nature of the predictions.

---

## 🏗️ Architecture & Tech Stack

- **Language:** Python 3.10+ (tested on Python 3.12)
- **Web Framework:** [Streamlit](https://streamlit.io/) (v1.30+)
- **Data Processing:** [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)
- **Visualization:** [Altair](https://altair-viz.github.io/) (interactive declarative charting)
- **Version Control:** Git & GitHub

### Project Structure
```text
stock-prediction-app/
├── .gitignore              # Ignores venv, caches, IDE configs, secrets
├── requirements.txt        # Python dependency manifest
├── README.md               # Project documentation and setup guide
├── app.py                  # Main Streamlit web application & UI layout
├── stock_data.py           # Hardcoded sample stock datasets & metrics
└── prediction.py           # Mathematical forecasting engine (OLS & SMA)
```

---

## ⚙️ Installation & Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.10 or higher installed. Check using:
```bash
python --version
```

### 2. Clone / Navigate to the Repository
```bash
cd stock-prediction-app
```

### 3. (Recommended) Create and Activate a Virtual Environment
- **Windows (Command Prompt / PowerShell):**
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

## 🚀 Running the Application

Launch the Streamlit web dashboard with:
```bash
streamlit run app.py
```

Once started, the application will automatically open in your default web browser at:
```
http://localhost:8501
```

---

## 🌿 Git Branching Strategy & Workflow

This project strictly follows feature branching to satisfy **LO2** requirements:

| Branch Name | Purpose | Merged Into |
|---|---|---|
| `main` | Production-ready, stable baseline application code | — |
| `feature/stock-dashboard` | Initial dataset structure, metrics, and Streamlit price dashboard | `main` |
| `feature/prediction-model` | OLS linear trend prediction engine, SMA indicators, and disclaimer | `main` |
| `feature/documentation` | Comprehensive README, project guides, and Git workflow docs | `main` |

### Git Workflow Commands Used:
```bash
# Initialize and configure repository
git init -b main
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Feature 1: Stock Dashboard
git switch -c feature/stock-dashboard
git add stock_data.py app.py
git commit -m "feat(dashboard): implement stock dataset module and Streamlit historical price dashboard"
git switch main
git merge --no-ff feature/stock-dashboard -m "merge: integrate feature/stock-dashboard into main"

# Feature 2: Prediction Model
git switch -c feature/prediction-model
git add prediction.py app.py
git commit -m "feat(prediction): implement mathematical trend projection model and educational disclaimer"
git switch main
git merge --no-ff feature/prediction-model -m "merge: integrate feature/prediction-model into main"

# Feature 3: Documentation
git switch -c feature/documentation
git add README.md
git commit -m "docs: add comprehensive README with setup guide, Git workflow, and architecture"
git switch main
git merge --no-ff feature/documentation -m "merge: integrate feature/documentation into main"
```

---

## 📐 Mathematical Methodology

### 1. Simple Moving Average (SMA)
For a time series of closing prices $P_t$, the $k$-day moving average is:
$$\text{SMA}_k(t) = \frac{1}{k} \sum_{i=0}^{k-1} P_{t-i}$$
Both **SMA-7** (weekly momentum) and **SMA-14** (bi-weekly trend) are calculated to identify moving trends.

### 2. Linear Trend Extrapolation
Given $n$ historical closing prices with discrete time indices $x_i \in \{0, 1, \dots, n-1\}$ and prices $y_i$:
$$y = m \cdot x + c$$
Where slope $m$ and intercept $c$ are solved via Ordinary Least Squares:
$$m = \frac{n \sum (x_i y_i) - \sum x_i \sum y_i}{n \sum x_i^2 - (\sum x_i)^2}$$
$$c = \frac{\sum y_i - m \sum x_i}{n}$$
Future days $x_f \in \{n, n+1, \dots, n+H-1\}$ are projected as $\hat{y}_f = m \cdot x_f + c$.

### 3. Illustrative Confidence Bands
Residual standard deviation $\sigma_\epsilon = \sqrt{\frac{1}{n} \sum (y_i - \hat{y}_i)^2}$ yields an illustrative 95% interval:
$$\text{Bounds} = \hat{y}_f \pm 1.96 \cdot \sigma_\epsilon$$

---

## ⚠️ Academic & Regulatory Disclaimer

> **IMPORTANT NOTICE:**  
> This application is strictly an **educational tool** developed for practical demonstration in **Agile Assignment No. 1**. The datasets, formulas, and price projections are illustrative mathematical approximations and do **not** reflect real-time financial market movements or live exchange feeds. Nothing in this application constitutes financial, investment, or legal advice.
