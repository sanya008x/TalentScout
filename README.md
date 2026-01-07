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

## 🧠 Prompt Engineering Strategy (Assignment Highlight)
The core logic of TalentScout relies on **iterative prompt engineering** rather than hardcoded logic.
1.  **State-Awareness**: The System Prompt includes a dynamic set of instructions that changes based on conversation history.
2.  **Information Extraction**: The LLM is instructed to parse user intent (e.g., if a user says "I am Bob, email is bob@co", it records both without asking).
3.  **Dynamic Branching**:
    - *Phase 1 (Info)*: The bot autonomously decides when it has enough info to move to Phase 2.
    - *Phase 2 (Technical)*: The bot generates questions *only* for the specific tech stack mentioned by the candidate (e.g., "Ask 3 Python questions" vs "Ask 3 Java questions").

## 🚧 Challenges & Solutions
- **Challenge**: The model would sometimes halluciation "NOTHING FOLLOWS" or system tags.
    - **Solution**: Implemented a string-cleaning post-processor in `utils.py` to strip these artifacts.
- **Challenge**: State management in a stateless Streamlit app.
    - **Solution**: Used `st.session_state` to persist the message history and fed the entire context back to the LLM on every turn.
- **Challenge**: Deployment specific API Keys.
    - **Solution**: Implemented a dual-check system (Secrets File + User Input) to ensure seamless usage locally and on cloud.

## 🛡️ License
Open Source. MIT License.
