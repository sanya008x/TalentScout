# 🚀 Deployment Guide for TalentScout (Local LLM Version)

Since this application uses **Ollama** running purely locally on your machine, you cannot simply deploy it to Streamlit Cloud or Heroku, as they do not have the GPU resources or permission to run persistent background LLM processes like Llama 3.

Here are your best options:

## Option 1: ⚡ Quick Demo via Ngrok (Easiest)
Use this to show the app to others temporarily while it runs on your laptop.

1.  **Run the downloaded Ngrok**:
    In the `TalentScout` directory:
    ```bash
    ./ngrok http 8502
    ```
    *(If it asks for an authtoken, sign up at dashboard.ngrok.com and run: `./ngrok config add-authtoken YOUR_TOKEN`)*
    ```bash
    streamlit run app.py
    ```
    (Note the port, usually 8501 or 8502)
3.  **Start Tunnel** (in a new terminal):
    ```bash
    ngrok http 8502
    ```
4.  **Share URL**: Ngrok will give you a generic URL (e.g., `https://random-name.ngrok-free.app`) that anyone can access.

---

## Option 2: ☁️ Deploy on GPU Cloud (AWS/GCP/Lambda Labs)
If you need a permanent server, you need a Virtual Machine (VM) with a GPU.

1.  **Rent a GPU Server**: Use Lambda Labs, AWS EC2 (g4dn.xlarge), or Google Cloud.
2.  **Install Dependencies** on the server:
    ```bash
    # Install Python & Pip
    sudo apt update && sudo apt install python3-pip
    
    # Install Ollama (Linux)
    curl -fsSL https://ollama.com/install.sh | sh
    ollama pull llama3
    
    # Clone your code
    git clone <your-repo-url>
    cd TalentScout
    pip install -r requirements.txt
    ```
3.  **Run as Service**:
    ```bash
    nohup streamlit run app.py --server.port 80 &
    ```

## Option 3: ☁️ Deploy Free on Cloud (Recommended)
To deploy on **Streamlit Cloud** or **Vercel**, you must use the Groq API (Cloud Brain) instead of local Ollama.

### Step 1: Get a Free Groq API Key
1.  Go to **[console.groq.com/keys](https://console.groq.com/keys)**.
2.  Login with Google or GitHub.
3.  Click **"Create API Key"**.
4.  Name it (e.g., `TalentScout`).
5.  **Copy the key** (it starts with `gsk_`). *You won't see it again.*

### How to avoid pasting the key every time?
You (and your users) do NOT need to paste the key every time. You can hardcode it safely using **Secrets**.

#### 1. For Local Use (Your Laptop)
Create a file at `.streamlit/secrets.toml` and add your key:
```toml
GROQ_API_KEY = "gsk_your_actual_api_key_here"
```
Now the app will auto-load it.

#### 2. For Streamlit Cloud (Public Deployment)
When you deploy to Streamlit Cloud, you want others to use **YOUR** key (so they don't have to pay or sign up).
1.  Push code to GitHub.
2.  On Streamlit Cloud, click **"Deploy"**.
3.  Click **"Advanced Settings"**.
4.  Paste the same TOML logic into the "Secrets" box:
    ```toml
    GROQ_API_KEY = "gsk_your_actual_api_key_here"
    ```
5.  Click "Save".

**Result**: Anyone who visits your public URL will use your hidden key automatically. They won't see the sidebar input box at all!

**Recommendation**: For this assignment/internship presentation, **Option 1 (Ngrok)** is the standard way to demo local AI apps without incurring cloud costs.
