# AegisDominus: Secure AI Defense System

![Datadog Monitored](https://img.shields.io/badge/Observability-Datadog-632CA6?style=flat-square&logo=datadog&logoColor=white)
![Python](https://img.shields.io/badge/Backend-Flask-blue?style=flat-square&logo=python&logoColor=white)
![Vertex AI](https://img.shields.io/badge/AI-Google%20Vertex%20AI-4285F4?style=flat-square&logo=googlecloud&logoColor=white)

## Overview

**AegisDominus** is a security-first AI proxy designed to protect Large Language Models (LLMs) from malicious misuse. It sits between the user and **Google Gemini**, providing real-time threat detection and granular observability that standard API calls lack.

**Key Capabilities:**
1.  **Active Defense:** Automatically detects and blocks "Jailbreak" attempts (e.g., prompt injection attacks) before they process.
2.  **Deep Observability:** Uses Datadog APM to trace every interaction, measuring token consumption, latency, and error rates per user.
3.  **Reliability Engineering:** Implements Service Level Objectives (SLOs) to guarantee 99% system uptime and performance.

## How it works

* **Core Backend:** Python (Flask)
* **AI Engine:** Google Vertex AI (`gemini-2.0-flash-001`)
* **Observability:** Datadog APM & Tracing

---

## Quick Start Guide

### Prerequisites
1.  **Google Cloud Project** with Vertex AI API enabled.
2.  **Datadog Account** (and API Key).
3.  **Google Cloud CLI (`gcloud`)** installed and authenticated. (its easier to download the exe file to install gcloud CLI).

### Step 1: Clone & Install

```bash
git clone https://github.com/PS-003R32/AegisDominus.git
cd AegisDominus

# Install dependencies
pip install -r requirements.txt
```
### Step 2: Google Cloud Authentication
Authenticate using your local Google credentials to access the Gemini model:
```bash
# Login to Google Cloud
gcloud auth application-default login

# Set your Project ID (Required for Vertex AI)
export PROJECT_ID="your-google-project-id" #create one and check in the settings
export LOCATION="us-central1"
```
### Step 3: Configure Datadog
Export your Datadog credentials directly in the terminal:
```bash
export DD_API_KEY="your_datadog_api_key_here"
export DD_SITE="us5.datadoghq.com"  # Check your account (e.g., datadoghq.com)
export DD_ENV="devpost-demo"
export DD_SERVICE="aegis-dominus"
```

### Step 4: Run the Application
Start the server using the Datadog Tracer wrapper to enable observability.
```bash
ddtrace-run python src/app.py
```
## Testing & Simulation
To demonstrate the security features, run the included traffic generator. This script simulates valid users and malicious attackers.
```bash
python traffic_generator.py
```

