import os
import json
from textblob import TextBlob
import PyPDF2
from groq import Groq
import streamlit as st

def get_groq_client():
    """Initializes Groq client with API Key from Secrets or Session State."""
    api_key = st.session_state.get("groq_api_key") or st.secrets.get("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def parse_resume_to_text(uploaded_file) -> str:
    """Extracts text from a generic PDF file object."""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_candidate_info_from_resume(resume_text: str) -> dict:
    """Uses LLM to extract structured info from resume text."""
    client = get_groq_client()
    if not client:
        return {}

    prompt = f"""
    Extract the following candidate information from the resume text below.
    Return the output ONLY as a valid JSON object with keys: 
    "full_name", "email", "phone", "experience", "role", "location", "tech_stack".
    If a field is not found, use null.
    
    RESUME TEXT:
    {resume_text[:6000]} 
    """
    
    try:
        # Using lightweight model for JSON extraction
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Extraction Error: {e}")
        return {}

def analyze_sentiment(text: str) -> dict:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        sentiment = "Positive"
        color = "green"
    elif polarity < -0.1:
        sentiment = "Negative"
        color = "red"
    else:
        sentiment = "Neutral"
        color = "gray"
        
    return {"score": polarity, "label": sentiment, "color": color}

EXIT_KEYWORDS = ["exit", "quit", "bye", "stop"]

def is_exit(user_input: str) -> bool:
    return any(word in user_input.lower() for word in EXIT_KEYWORDS)

def get_llm_response(messages: list) -> str:
    """Sends conversation context to Groq API."""
    client = get_groq_client()
    if not client:
        return "⚠️ API Key missing. Please enter your Groq API Key in the sidebar."

    # Convert format if needed, but Groq accepts list of dicts {role, content}
    # We just need to ensure 'system' role is valid (it is for Llama3 on Groq)
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Using latest 70b for better intelligence
            messages=messages,
            temperature=0.6,
            max_tokens=1024
        )
        response_text = completion.choices[0].message.content.strip()
        
        # Post-processing filters
        blocklist = [
            "NOTHING FOLLOWS YET", "NOTHING FOLLOWS", 
            "LANGUAGE INSTRUCTIONS", "PHASE 1: INFORMATION GATHERING",
            "PHASE 2: TECHNICAL SCREENING", "PHASE 3: CONCLUSION",
            "### LANGUAGE INSTRUCTIONS", "### PHASE 1: INFORMATION GATHERING"
        ]
        
        for phrase in blocklist:
            response_text = response_text.replace(phrase, "")
            
        return response_text
    except Exception as e:
        return f"Error connecting to Groq API: {str(e)}"

def generate_feedback(messages: list) -> str:
    """Generates a performance scorecard."""
    client = get_groq_client()
    if not client:
        return "Error: API Key missing."

    prompt = "Review the following interview transcript and provide a detailed structured feedback report.\n\n"
    for msg in messages:
         if msg["role"] == "user":
             prompt += f"Candidate: {msg['content']}\n"
         elif msg["role"] == "assistant":
             prompt += f"Interviewer: {msg['content']}\n"
             
    prompt += """
    OUTPUT FORMAT:
    # 📝 Interview Feedback Report
    ## 📊 Score: [1-10]/10
    ## ✅ Strengths ...
    ## ⚠️ Areas for Improvement ...
    ## 🏁 Final Decision ...
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating feedback: {str(e)}"