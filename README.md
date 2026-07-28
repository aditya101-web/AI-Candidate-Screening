# 🤖 AI Candidate Screening Platform

> An AI-powered recruitment platform that automates the candidate screening process using Large Language Models (Gemini AI), GitHub profile analysis, resume parsing, and interview scheduling.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-WebApp-red)
![Gemini](https://img.shields.io/badge/Google-Gemini_AI-green)
![Google Calendar](https://img.shields.io/badge/Google-Calendar-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

# 📌 Overview

Hiring the right candidate is a time-consuming process involving resume screening, technical evaluation, GitHub profile analysis, email communication, and interview scheduling.

This project automates the complete recruitment workflow using AI.

The platform allows recruiters to:

- Upload candidate datasets
- Download and parse resumes
- Evaluate resumes using Gemini AI
- Analyze GitHub profiles
- Rank candidates automatically
- Upload coding assessment results
- Send interview invitation emails
- Schedule Google Meet interviews

---

# 🚀 Features

### 📂 Candidate Dataset Management

- Upload candidate dataset (CSV/Excel)
- Preview uploaded candidates
- Manage candidate information

---

### 📄 Resume Processing

- Automatic resume downloading
- Resume parsing
- Text extraction from PDF resumes

---

### 🤖 AI Resume Evaluation

Powered by **Google Gemini AI**

Evaluates:

- Technical Skills
- Project Experience
- Education
- Certifications
- Problem Solving Ability
- Job Description Matching

Generates:

- Resume Score (0–100)
- Candidate Summary
- Hiring Recommendation

---

### 💻 GitHub Profile Analysis

Automatically analyzes candidate GitHub profiles.

Evaluates:

- Repository Quality
- Programming Languages
- Technical Projects
- Open Source Activity
- Documentation Quality
- Developer Consistency

Produces:

- GitHub Score
- Strengths
- Weaknesses
- Technical Skills
- Hiring Recommendation

---

### 🏆 Candidate Ranking

Ranks candidates using:

- Resume Score
- GitHub Score
- Coding Assessment Score

Displays:

- Technical Interview
- HR Interview
- Reject

---

### 📧 Email Automation

Automatically sends interview assessment emails to shortlisted candidates using Gmail SMTP.

---

### 📅 Google Calendar Integration

Automatically schedules interviews.

Features:

- Google Calendar Event Creation
- Google Meet Link Generation
- Candidate Invitation

---

### 📊 Dashboard

Interactive Streamlit dashboard including:

- Candidate Statistics
- Ranking Table
- AI Recommendations
- Score Visualization
- Candidate Comparison

---

# 🛠 Tech Stack

| Category | Technologies |
|-----------|--------------|
| Frontend | Streamlit |
| Backend | Python |
| AI | Google Gemini API |
| Resume Parsing | PyMuPDF |
| Data Processing | Pandas |
| Visualization | Plotly |
| GitHub Analysis | GitHub REST API |
| Authentication | Google OAuth 2.0 |
| Calendar | Google Calendar API |
| Email | Gmail SMTP |

---

# 📁 Project Structure

```
AI-Candidate-Screening/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── credentials.json
│
├── assets/
├── data/
├── outputs/
├── resumes/
│
└── modules/
    ├── ai_scoring.py
    ├── calendar_scheduler.py
    ├── dataset.py
    ├── email_sender.py
    ├── fallback_scoring.py
    ├── github_ai.py
    ├── github_analysis.py
    ├── process_candidates.py
    ├── ranking.py
    ├── resume_downloader.py
    └── resume_parser.py
```

---

# 🔄 System Workflow

```
Candidate Dataset
        │
        ▼
Resume Download
        │
        ▼
Resume Parsing
        │
        ▼
Gemini AI Evaluation
        │
        ▼
GitHub Analysis
        │
        ▼
Candidate Ranking
        │
        ▼
Coding Assessment Upload
        │
        ▼
Final Ranking
        │
        ▼
Interview Email
        │
        ▼
Google Calendar Scheduling
        │
        ▼
Google Meet Link
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/AI-Candidate-Screening.git
```

Move into the project

```bash
cd AI-Candidate-Screening
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

EMAIL_ADDRESS=YOUR_EMAIL

EMAIL_PASSWORD=YOUR_APP_PASSWORD
```

---

# 🔐 Google Calendar Setup

1. Create a Google Cloud Project.
2. Enable Google Calendar API.
3. Configure OAuth Consent Screen.
4. Download `credentials.json`.
5. Place it in the project root.
6. Run the application.
7. Sign in once to authorize access.

---

# 📷 Application Screenshots

## Home Page

_Add Screenshot_

---

## Dataset Upload

_Add Screenshot_

---

## AI Resume Screening

_Add Screenshot_

---

## Candidate Ranking

_Add Screenshot_

---

## GitHub Analysis

_Add Screenshot_

---

## Google Meet Scheduler

_Add Screenshot_

---

# 📈 Future Improvements

- PostgreSQL Database
- Multi-user Authentication
- ATS Integration
- Docker Deployment
- Resume OCR
- AI Interview Chatbot
- Analytics Dashboard
- Candidate Skill Gap Analysis

---

# 👨‍💻 Author

**Aditya Shukla**

B.Tech Computer Science Engineering (AI & ML)

K.R. Mangalam University

GitHub: https://github.com/aditya101-web

LinkedIn: https://www.linkedin.com/in/aditya-shukla-6000162a3/

---

# ⭐ If you found this project useful, consider giving it a star!