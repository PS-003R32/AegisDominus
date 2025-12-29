# AegisDominus
![Datadog Monitored](https://img.shields.io/badge/Monitored%20by-Datadog-632CA6?style=flat-square&logo=datadog&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)
![Gemini AI](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?style=flat-square&logo=google&logoColor=white)
- Secure AI Assistant with Full Observability.
- A secure, monitored LLM application powered by **Google Gemini** and observed by **Datadog**.

---
## Overview

**AegisDominus** is a proof-of-concept for a *Secure AI Pipeline*. In an era where "Jailbreaking" LLMs is a major risk, AegisDominus implements a defense-in-depth strategy:

1.  **Application Layer:** Real-time input validation to block prompt injection attacks.
2.  **Observability Layer:** A Datadog dashboard that tracks token usage, latency, and security incidents.
3.  **Reliability Layer:** An automated SLO (Service Level Objective) tracking system to ensure 99% uptime.

## Features

* **AI-Powered:** integrated with Google Gemini Pro for intelligent responses.
* **Jailbreak Defense:** Automatically detects and blocks "Ignore previous instructions" and other prompt injection attempts (returns `403 Forbidden`).
* **Real-Time Dashboard:** Visualizes traffic volume, error rates, and AI token consumption.
* **Automated Security Alerts:** Triggers critical alerts when attack patterns are detected.
* **SLO Tracking:** Monitors reliability with a 99% uptime target using Datadog Monitors.

## Tech Stack

* **Backend:** Python (Flask)
* **AI Model:** Google Generative AI (Gemini)
* **Observability:** Datadog APM & Trace
* **Simulation:** Custom Python Traffic Generator

---
## The Dashboard

Our **Datadog Command Center** provides a single pane of glass for both Operations and Security.

### 1. The "Healthy" State
*Traffic is flowing normally. SLO badge is green (99%).*
### 2. Attack Detection (The "Red" State)
*A jailbreak attempt is detected. The **Security Incidents** graph spikes RED, and the **Monitor Summary** triggers an ALERT.*

---
### Prerequisites
* Python 3.10+
* A Datadog API Key
* A Google Gemini API Key

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/PS-003R32/AegisDominus.git
    cd AegisDominus
    ```
2.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```ini
    DD_API_KEY=your_datadog_api_key
    DD_SITE=us5.datadoghq.com  # or your specific datadog site
    GOOGLE_API_KEY=your_gemini_api_key
    DD_SERVICE=Aegis-Dominus-app
    DD_ENV=production
    ```
### Usage
**Terminal 1: Start the Secure App**
This runs the Flask server wrapped in the Datadog Tracer.
```bash
ddtrace-run python src/app.py
```
**Terminal 2:** Run Traffic Simulation This script simulates normal users AND malicious attackers to demonstrate the dashboard's capabilities.
```bash
python traffic_generator.py
```
## How It Works
1. The Trap: The application code (app.py) scans every incoming prompt.

2. The Trigger: If a prompt contains restricted keywords (e.g., "Ignore previous instructions"), the app aborts the request with a 403 Forbidden error.

3. The Trace: Datadog APM captures this 403 error and tags it with metadata.

4. The Alert: A Datadog Monitor watches for status:403 spikes. If detected, it updates the dashboard and sends an alert.

