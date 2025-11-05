# 🧠 AI Lead Generation System

A comprehensive **AI-powered lead generation platform** that automates company research, business summarization, and personalized outreach email creation using advanced AI and web technologies.

---

## 📘 Overview

The **E2M AI Lead Generation System** transforms how businesses approach lead research and outreach by leveraging artificial intelligence to:

- 🤖 Automatically research companies and extract key information  
- 🧩 Generate intelligent business summaries using **Groq AI**  
- ✉️ Create personalized outreach emails tailored to each company  
- 📊 Provide comprehensive analytics on lead generation performance  
- 🖥️ Offer a professional web interface for easy management  

---

## ✨ Features

### 🤖 AI-Powered Intelligence
- **Smart Business Summaries:** AI-generated 2–3 sentence company summaries  
- **Personalized Email Creation:** Context-aware outreach email generation  
- **Domain Extraction:** Automatic extraction from emails and websites  
- **Content Analysis:** Intelligent web content processing  

### 🎨 Professional Web Interface
- **4 Interactive Pages:** Home, Dashboard, Results, Analytics  
- **Responsive Design:** Works perfectly on desktop, tablet, and mobile  
- **Real-Time Progress:** Animated progress indicators and status updates  
- **Beautiful Charts:** Interactive analytics with Chart.js  

### ⚡ Advanced Functionality
- **Industry Filtering:** Target specific industries (Tech, Healthcare, Finance, etc.)  
- **Multiple Email Templates:** Partnership, Collaboration, Service Introduction  
- **Performance Analytics:** Track success rates, processing times, and metrics  
- **Export Capabilities:** Export results for further processing  
- **Error Handling:** Comprehensive error logging and recovery  

---

## 📊 Analytics & Reporting
- **Real-Time Metrics:** Live tracking of leads processed, success rates, errors  
- **Interactive Dashboards:** Visual charts for performance monitoring  
- **Historical Data:** Daily statistics and trend analysis  
- **Processing Insights:** Average processing times and efficiency metrics  

---

## 🚀 Quick Start

### 🧩 Prerequisites
- Python 3.8 or higher  
- Groq API account (free tier available)  
- Modern web browser  

### ⏱️ 5-Minute Setup
1. **Clone or Download** the project files  
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
    ```

Configure API Keys in .env file

Run the Application:
```
python app.py
```


Open in Browser:
👉 http://localhost:5000


# ⚙️ Installation
Step 1: Environment Setup
### Create project directory
mkdir E2M_Lead_Generator
cd E2M_Lead_Generator

### Create virtual environment (recommended)
python -m venv venv
### On Windows
    venv\Scripts\activate
### On Linux/Mac
    source venv/bin/activate

Step 2: Install Dependencies

    pip install -r requirements.txt

Step 3: API Configuration

Create a .env file with your API keys:

### Required: Get from https://console.groq.com/
GROQ_API_KEY=gsk_your_actual_groq_api_key_here

### Optional: For production lead data
APIFY_API_KEY=your_apify_api_key_here

### Application Settings
DEBUG=True
MAX_LEADS=20

Step 4: Verify Installation
python quick_test.py


Expected Output:

🧪 E2M AI Lead Generation - Environment Test
==================================================
🔑 Groq API Key: ✅ Found
🔑 Apify API Key: ❌ Missing (Using demo data)

🚀 Quick Start:
   1. python app.py
   2. Visit: http://localhost:5000

🎮 Usage
Starting the Application

    python app.py


You’ll See:

🚀 E2M AI Lead Generation Web Application
==================================================
✅ Groq API: Connected
✅ Apify API: Not Configured (Using demo data)
🌐 Starting server on http://localhost:5000

Web Interface Navigation

Homepage (/): Lead generation workflow

Dashboard (/dashboard): Performance overview

Analytics (/analytics): Charts and metrics

Results (/results): Processing outcomes

Generating Leads

---

Set Parameters:

Number of leads (1–10)

Industry filter (All, Technology, Healthcare, etc.)

Email type (Partnership, Collaboration)

---

Start Processing:

Click "Generate AI Leads"

Watch real-time progress

View detailed results

---

Review Output:

Business summaries

Personalized emails

Processing metrics

Export options

---

# 🔄 Workflow Process
Step 1: Lead Data Collection

* Input: Company names, emails, websites

* Source: Apify API or demo database

* Output: Raw lead data with contact information

Step 2: Domain Extraction

* Process: Extract domains from emails and websites

* Logic: Direct domain → Email domain → Website URL

* Output: Clean domain names for scraping

Step 3: Web Content Scraping

* Action: Scrape company website content

* Method: BeautifulSoup for HTML parsing

* Output: Website text content for analysis

Step 4: AI Business Summarization

* Model: Groq Mixtral-8x7b-32768

* Input: Company name, domain, website content

* Output: 2–3 sentence professional summary

Step 5: Email Generation

* Templates: Partnership, Collaboration, Service Introduction

* Personalization: Company-specific context

* Output: Ready-to-send outreach emails

Step 6: Results Compilation

* Metrics: Processing times, success rates, errors

* Analytics: Performance tracking and insights

* Export: Results available for download

# 🖼️ Screenshots

<img width="1920" height="1080" alt="Screenshot 2025-11-05 092728" src="https://github.com/user-attachments/assets/b43bc8f2-ea87-49dd-ba04-695ae3d42358" />

<img width="1920" height="1080" alt="Screenshot 2025-11-05 092736" src="https://github.com/user-attachments/assets/6b05ab70-a36c-4ac3-b20f-9901d0098dc4" />

<img width="1920" height="1080" alt="Screenshot 2025-11-05 092942" src="https://github.com/user-attachments/assets/4e1071b3-f415-45cc-9224-9b8099275f4d" />

<img width="1920" height="1080" alt="Screenshot 2025-11-05 092958" src="https://github.com/user-attachments/assets/5d48d5b0-16d3-40f7-a3ea-814a81da8252" />

<img width="1920" height="1080" alt="Screenshot 2025-11-05 093010" src="https://github.com/user-attachments/assets/14bcabe5-b11f-457f-b6f2-bcd90b58b892" />

<img width="1920" height="1080" alt="Screenshot 2025-11-05 093028" src="https://github.com/user-attachments/assets/b47ef6bb-fed0-4b3c-aadc-dcda3723215b" />

<img width="1920" height="1080" alt="Screenshot 2025-11-05 093042" src="https://github.com/user-attachments/assets/0907796a-8f94-485f-9316-cd7eaf2f1fc3" />


