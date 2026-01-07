# TalentScout Hiring Assistant 🤖
> **An Intelligent, Cloud-Ready AI Interviewer built with Streamlit & LLaMA 3.**

TalentScout is a smart hiring assistant designed to screen candidates efficiently. It engages users in a natural conversation to gather details, parses uploaded resumes, dynamically generates technical questions based on the user's stack, and provides a structured feedback report at the end.

## ✨ Key Features
- **🧠 Cloud Brain**: Powered by **LLaMA 3 (via Groq API)** for lightning-fast, intelligent responses.
- **📄 AI Resume Parser**: Upload a PDF resume, and the AI extracts key details (Name, Stack, Experience) automatically.
- **⚡ Dynamic Questioning**: No hardcoded scripts. The AI generates relevant technical questions based on the candidate's specific tech stack.
- **📊 Instant Feedback**: Generates a structured scorecard (Strengths, Weaknesses, Hire/No-Hire) after the interview.
- **🔐 Secure Deployment**: Uses standard Secret Management to keep API keys safe.

---

## 🚀 Quick Start (Cloud Mode)

### 1. Prerequisites
- Python 3.8+
- A free API Key from [Groq Console](https://console.groq.com/keys).

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/TalentScout.git
cd TalentScout

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration (Secrets)
Create a file named `.streamlit/secrets.toml` in the project folder to save your key securely:
```toml
# .streamlit/secrets.toml
GROQ_API_KEY = "gsk_your_actual_key_here"
```
*(This prevents you from having to paste the key every time you run the app).*

### 4. Run the App
```bash
streamlit run app.py
```
Visit `localhost:8502` in your browser.

---

## ☁️ Deployment (Streamlit Cloud)
This project is ready for one-click deployment.

1.  Push your code to **GitHub**.
2.  Go to [Streamlit Community Cloud](https://share.streamlit.io).
3.  Deploy the repository.
4.  **Crucial Step**: In the "Advanced Settings" -> "Secrets" menu, paste your API key:
    ```toml
    GROQ_API_KEY = "gsk_your_actual_key_here"
    ```
5.  Click Deploy! 🚀

---

## 🛠️ Technical Architecture
- **Frontend**: Streamlit (Python).
- **AI Model**: LLaMA-3-70b/8b via **Groq Cloud API**.
- **PDF Extraction**: `PyPDF2` + `llama-3.1-8b-instant` for structured extraction.
- **State Management**: `st.session_state` for conversation history.

### Directory Structure
```
TalentScout/
├── app.py              # Main Application Logic
├── utils.py            # AI Engine (Groq Client, Resume Parser)
├── prompts.py          # System Instructions & Persona
├── requirements.txt    # Dependencies
├── .streamlit/         # Secrets & Config
│   └── secrets.toml    # (IGNORED by Git) API Keys
└── assets/             # Images/Logos
```

## 🛡️ License
Open Source. MIT License.
