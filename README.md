# TalentScout Hiring Assistant

## Project Overview
TalentScout is an intelligent, LLM-driven Hiring Assistant chatbot designed to screen candidates. It engages users in a conversation to gather essential details (Name, Experience, Tech Stack, etc.) and dynamically generates technical screening questions based on the declared technology stack.

## Installation Instructions
1. **Prerequisites**:
   - Python 3.8+
   - [Ollama](https://ollama.com/) installed and running.
   - LLaMA 3 model pulled (`ollama pull llama3`).
   - **Verification**: Run `ollama list` in your terminal to ensure `llama3` is available.

2. **Setup**:
   ```bash
   # Clone the repository (if applicable)
   # git clone <repo-url>
   # cd TalentScout

   # Create and activate virtual environment
   # Mac/Linux:
   python3 -m venv venv
   source venv/bin/activate
   # Windows:
   # python -m venv venv
   # .\venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Running the Application**:
   Ensure Ollama is running in the background.
   ```bash
   streamlit run app.py
   ```

## Usage Guide
- Launch the app using `streamlit run app.py`.
- The chatbot will greet you.
- Provide the requested information (Name, Email, etc.) naturally.
- Once you declare your tech stack, the assistant will generate technical questions.
- Type "exit" or "bye" at any time to end the conversation.
- Use the **"🔄 Reset Conversation"** button in the sidebar to start a new interview session instantly.

## Technical Details
- **Frontend**: Streamlit
- **LLM**: LLaMA 3 (via Ollama local inference)
- **Architecture**: 
    - `app.py`: Main Streamlit UI and event loop.
    - `prompts.py`: Contains the System Prompt that defines the persona and logic.
    - `utils.py`: Handles communication with the local Ollama instance.
- **Data Handling**: Session-based ephemeral storage. No persistent database is used, complying with privacy requirements for this demo.

## Prompt Design
The core logic resides in a structured **System Prompt** (`prompts.py`). Instead of hardcoded if/else statements, we utilize the instruction following capabilities of LLaMA 3. 
- **Information Gathering**: The LLM is instructed to check history and only ask for missing fields one by one.
- **Dynamic Questioning**: The prompt detects when the "Tech Stack" is provided and triggers the "Technical Screening Questions" section.
- **Safety**: Robust constraints prevent the bot from deviating from its role.

## Challenges & Solutions
- **State Management**: Handling the state in a stateless LLM call layout was solved by feeding the entire valid conversation history back to the model on every turn.
- **Prompt Adherence**: Ensuring the model asks one question at a time required specific negative constraints ("Do NOT ask for everything at once").
