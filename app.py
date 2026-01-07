import streamlit as st
from prompts import SYSTEM_PROMPT
from utils import get_llm_response, is_exit, analyze_sentiment, generate_feedback, parse_resume_to_text, extract_candidate_info_from_resume

st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="assets/logo.png",
    layout="centered"
)

# Custom CSS for "Premium" Aesthetics (Light Theme)
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif;
        color: #0F172A;
    }

    /* Chat Messages */
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #E0E7FF;
        margin-bottom: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* User Message - Primary Color */
    .stChatMessage[data-testid="user-message"] {
        background-color: #2563EB;
        color: white !important;
        border: none;
    }
    
    /* Force text color in user message to be white */
    .stChatMessage[data-testid="user-message"] p {
        color: white !important;
    }

    /* Input Box */
    .stChatInputContainer {
        border-color: #2563EB !important;
    }

    /* Header */
    h1 {
        color: #0F172A !important;  /* Changed to Near Black */
        font-weight: 700 !important;
    }
    
    /* Sidebar Button */
    .stButton button {
        background-color: #64748B; /* Secondary Slate Gray */
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
    }
    .stButton button:hover {
        background-color: #475569;
        color: white;
        border-color: transparent;
    }
    
</style>
""", unsafe_allow_html=True)

# Sidebar for controls
# Sidebar for controls
with st.sidebar:
    # Check for API Key in Secrets or Session State
    if "GROQ_API_KEY" in st.secrets:
        # Subtle indicator instead of big green box
        st.markdown("🔒 *API Key secured via Secrets*")
    elif "groq_api_key" in st.session_state:
        st.markdown("🔑 *API Key configured*")
    else:
        st.subheader("🔑 API Configuration")
        api_key_input = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
        if api_key_input:
            st.session_state.groq_api_key = api_key_input
            st.rerun()

    st.header("⚙️ Settings")
    
    # Language Selector
    language = st.radio(
        "Preferred Language",
        ["English", "Spanish", "French", "German", "Hindi", "Auto-Detect"],
        index=0
    )
    
    st.divider()
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"], key="resume_uploader")
    
    if uploaded_file and "resume_processed" not in st.session_state:
        with st.spinner("Analyzing Resume..."):
            text = parse_resume_to_text(uploaded_file)
            data = extract_candidate_info_from_resume(text)
            
            if data:
                # Update session state with extracted info
                if "candidate_data" not in st.session_state:
                    st.session_state.candidate_data = {}
                st.session_state.candidate_data.update(data)
                
                # Construct a system injection to inform the LLM of known info
                known_info = f"\n\n[SYSTEM UPDATE]: The candidate has uploaded a resume. The following information is already known: {data}. DO NOT ask for this information again. Confirm with the candidate what you have found."
                
                # Update the conversation history to include this context
                if st.session_state.messages:
                    st.session_state.messages[0]['content'] += known_info
                
                st.session_state.resume_processed = True
                st.success("Resume Parsed Successfully!")
                st.rerun()

    st.divider()
    st.subheader("📊 Interview Insights")
    if "sentiment_history" in st.session_state and st.session_state.sentiment_history:
        last = st.session_state.sentiment_history[-1]
        st.metric("Candidate Sentiment", last['label'], delta=f"{last['score']:.2f}")
    else:
        st.info("Waiting for candidate input...")
    
    st.divider()
    
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = []
        st.session_state.sentiment_history = []
        st.session_state.phase = "active"
        st.rerun()

# Initialize session state
if "messages" not in st.session_state or not st.session_state.messages:
    # Set the system prompt with language instruction
    lang_instruction = ""
    if language != "Auto-Detect":
        if language == "English":
            lang_instruction = "\nIMPORTANT: You must conduct the entire interview in English."
        else:
            lang_instruction = f"\nIMPORTANT: You must conduct the entire interview in {language}. Do NOT use English. Do NOT provide translations."

    # Start with the system prompt and an initial greeting from the assistant
    initial_greeting = "Hello! I am the TalentScout Hiring Assistant. I'm here to learn a bit about your background and technical skills. To start, could you please tell me your full name?"
    
    # If language is not English/Auto, we might want the greeting to be translated by the LLM, 
    # but for simplicity in this demo, we'll keep the initial static greeting 
    # and let the LLM take over from the first interaction, OR we can make the LLM generate the greeting.
    # A better approach for "Initial Greeting" in a specific language:
    # We will rely on the System Prompt to enforce language for *future* messages.
    # But the FIRST message is hardcoded. 
    # Let's leave the hardcoded one in English as a default, 
    # but append a system note to `SYSTEM_PROMPT` inside the message list.
    
    current_system_prompt = SYSTEM_PROMPT + lang_instruction

    st.session_state.messages = [
        {"role": "system", "content": current_system_prompt},
        {"role": "assistant", "content": initial_greeting}
    ]
    st.session_state.phase = "active"

# Header with Logo
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.png", width=80)
with col2:
    st.title("TalentScout Hiring Assistant")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(msg["content"])

# Chat Input
user_input = st.chat_input("Type your response here...")

if user_input and st.session_state.phase != "completed":
    # 1. Analyze Sentiment
    sentiment = analyze_sentiment(user_input)
    if "sentiment_history" not in st.session_state:
        st.session_state.sentiment_history = []
    st.session_state.sentiment_history.append(sentiment)

    # 2. Handle User Input
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Check for Exit or Conclusion
    # We check if the assistant's LAST message was a conclusion (e.g. contains "Thank you" or similar after questions)
    # But strictly for "exit" command:
    if is_exit(user_input):
        farewell = "Thank you for your time. Generating your feedback report..."
        with st.chat_message("assistant"):
            st.write(farewell)
        st.session_state.messages.append({"role": "assistant", "content": farewell})
        
        # ARCADE MODE: Feedback Generation
        with st.spinner("Analyzing your interview performance..."):
            feedback = generate_feedback(st.session_state.messages)
        
        st.markdown(feedback)
        st.session_state.messages.append({"role": "assistant", "content": feedback})
        
        st.session_state.phase = "completed"
        st.stop()

    # 3. Get LLM Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            assistant_reply = get_llm_response(st.session_state.messages)
            st.write(assistant_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    
    # Check if the assistant just concluded the interview (Phase 3 Conclusion)
    # Heuristic: If it says "Thank you" and "recruitment team will review"
    if "recruitment team will review" in assistant_reply.lower() or "thank you for your time" in assistant_reply.lower():
         with st.spinner("Generating interview feedback..."):
            feedback = generate_feedback(st.session_state.messages)
            st.markdown(feedback)
            st.session_state.messages.append({"role": "assistant", "content": feedback})
            st.session_state.phase = "completed"
            st.stop()