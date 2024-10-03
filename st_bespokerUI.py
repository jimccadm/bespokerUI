import streamlit as st
import requests
import re
import ollama
import subprocess
import time
from datetime import datetime

MODEL_NAME = "bespoke-minicheck"

def check_ollama_installation():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
    except FileNotFoundError:
        pass
    return False, ""

def get_available_models():
    try:
        response = ollama.list()
        if isinstance(response, dict) and 'models' in response:
            models = [model['name'] for model in response['models']]
            return models
        else:
            return []
    except Exception as e:
        return []

def check_model_exists(model_name):
    try:
        result = subprocess.run(["ollama", "show", model_name], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        return False

def clean_text(text):
    cleaned = re.sub(r'["\']', '', text)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def generate_answer(context, question):
    cleaned_context = clean_text(context)
    cleaned_question = clean_text(question)
    prompt = f"""Given the following context, please answer the question with ONLY 'Yes' or 'No'. Do not provide any explanation.

Context: {cleaned_context}

Question: {cleaned_question}

Answer (Yes/No):"""
    
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        result = response.json()
        full_answer = result.get('response', '').strip().lower()
        
        if 'yes' in full_answer:
            return 'YES', prompt, result
        elif 'no' in full_answer:
            return 'NO', prompt, result
        else:
            return 'UNCLEAR', prompt, result
    except Exception as e:
        return None, prompt, str(e)

def display_answer(answer):
    if answer == 'YES':
        color = '#28a745'  # Softer green
    elif answer == 'NO':
        color = '#dc3545'  # Softer red
    else:
        color = '#ffc107'  # Softer yellow/orange

    st.markdown(f"""
    <h2 style='text-align: center; color: {color}; font-size: 48px; font-weight: 500;'>
        {answer}
    </h2>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide")
    
    # CSS for improved typography, column separators, icons, and pulsing effect
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 400;
        color: #333;
    }
    h1 {
        font-size: 24px;
        font-weight: 600;
        color: #1e1e1e;
        margin-bottom: 1rem;
    }
    h2 {
        font-size: 20px;
        font-weight: 500;
        color: #1e1e1e;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    h3 {
        font-size: 18px;
        font-weight: 500;
        color: #1e1e1e;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .column-separator {
        border-right: 1px solid #e0e0e0;
        height: 100vh;
        position: absolute;
        top: 0;
        right: 0;
    }
    .stButton>button {
        background-color: #f0f2f6;
        color: #1e1e1e;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stTextArea>div>div>textarea {
        font-size: 14px;
    }
    .stAlert {
        font-size: 14px;
    }
    .icon-button {
        background: none;
        border: none;
        color: #1e1e1e;
        font-size: 20px;
        cursor: pointer;
        margin-left: 10px;
    }
    .icon-button:hover {
        color: #4a4a4a;
    }
    .title-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    @keyframes pulse {
        0% {
            opacity: 0.6;
        }
        50% {
            opacity: 1;
        }
        100% {
            opacity: 0.6;
        }
    }
    .analysing {
        animation: pulse 1.5s infinite;
        color: #ffa500;
        font-weight: 500;
    }
    .completed {
        color: #28a745;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # JavaScript for print functionality
    st.markdown("""
    <script>
    function printContent() {
        var context = document.getElementById('context').value;
        var question = document.getElementById('question').value;
        var answer = document.querySelector('.stMarkdown h2').innerText;
        var explanation = document.getElementById('answer-explanation').innerText;
        
        var printWindow = window.open('', '_blank');
        printWindow.document.write('<html><head><title>Print</title>');
        printWindow.document.write('</head><body>');
        printWindow.document.write('<h2>Context:</h2><p>' + context + '</p>');
        printWindow.document.write('<h2>Question:</h2><p>' + question + '</p>');
        printWindow.document.write('<h2>Answer:</h2><p>' + answer + '</p>');
        printWindow.document.write('<h2>Answer Explanation:</h2><p>' + explanation + '</p>');
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Create three columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h1>Ollama Configuration</h1>", unsafe_allow_html=True)
        
        # Initialize session state for Ollama status and models
        if 'ollama_installed' not in st.session_state:
            st.session_state.ollama_installed, _ = check_ollama_installation()
        if 'available_models' not in st.session_state:
            st.session_state.available_models = get_available_models() if st.session_state.ollama_installed else []
        if 'refresh_time' not in st.session_state:
            st.session_state.refresh_time = time.time() - 10
        if 'refresh_datetime' not in st.session_state:
            st.session_state.refresh_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Status
        if st.session_state.ollama_installed:
            st.success("Ollama Installation: Installed")
        else:
            st.error("Ollama Installation: Not Found")
        
        # Refresh button
        if st.button("🔄 Refresh Models"):
            st.session_state.ollama_installed, _ = check_ollama_installation()
            st.session_state.available_models = get_available_models() if st.session_state.ollama_installed else []
            st.session_state.refresh_time = time.time()
            st.session_state.refresh_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        st.markdown("<h2>Available Models:</h2>", unsafe_allow_html=True)
        if st.session_state.available_models:
            for model in st.session_state.available_models:
                if model == MODEL_NAME:
                    st.markdown(f"- <span style='color: #28a745; font-weight: 500;'>{model} (active)</span>", unsafe_allow_html=True)
                else:
                    st.write(f"- {model}")
        else:
            st.write("No models found or unable to retrieve model list.")

        # Check if the hardcoded model exists
        model_exists = check_model_exists(MODEL_NAME)
        st.write(f"Debug - {MODEL_NAME} exists: {model_exists}")

        # Fading "Models Refreshed" message with timestamp
        time_since_refresh = time.time() - st.session_state.refresh_time
        opacity = max(0, 1 - (time_since_refresh / 5))  # Fade over 5 seconds
        st.markdown(
            f"""
            <div style="opacity: {opacity}; transition: opacity 0.5s ease-in-out; font-size: 12px; color: #666;">
                Models Refreshed on {st.session_state.refresh_datetime}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Add column separator
        st.markdown('<div class="column-separator"></div>', unsafe_allow_html=True)

    with col2:
        # Title with Print and Reset icons
        st.markdown("""
        <div class="title-container">
            <h1>Yes/No Question Answering</h1>
            <div>
                <button onclick="printContent()" class="icon-button" title="Print">🖨️</button>
                <button onclick="window.location.reload()" class="icon-button" title="Reset">🔄</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if 'answer' not in st.session_state:
            st.session_state.answer = None
        if 'analysing' not in st.session_state:
            st.session_state.analysing = False

        context = st.text_area(
            "Enter the context:",
            height=200,
            help="Enter the context here that you want to test. Do NOT ask a question here, just copy and paste the body of text, paragraph, multi-paragraph or document here.",
            key="context"
        )
        question = st.text_area(
            "Enter your yes/no question:",
            height=70,
            help="Here, enter the question you want to pose against the data. Example: The context provided talks about War. The bespoke-minicheck LLM only ever replies with Yes or No.",
            key="question"
        )
        
        col_check, col_status = st.columns([1, 4])
        
        with col_check:
            check_button = st.button("Check")
        
        with col_status:
            if st.session_state.analysing:
                st.markdown('<span class="analysing">Analysing...please wait</span>', unsafe_allow_html=True)
            elif st.session_state.answer is not None:
                st.markdown('<span class="completed">Completed</span>', unsafe_allow_html=True)
        
        if check_button:
            if not st.session_state.ollama_installed:
                st.error("Ollama is not installed or not running. Please install Ollama to use this application.")
            elif MODEL_NAME not in st.session_state.available_models and not model_exists:
                st.error(f"The required model '{MODEL_NAME}' is not available. Please install it using 'ollama pull {MODEL_NAME}'")
            elif context and question:
                st.session_state.analysing = True
                st.session_state.answer = None
                st.rerun()
            else:
                st.warning("Please provide both context and a question.")

        if st.session_state.analysing:
            st.session_state.answer, st.session_state.prompt, st.session_state.result = generate_answer(context, question)
            st.session_state.analysing = False
            st.rerun()

        if st.session_state.answer:
            display_answer(st.session_state.answer)

        # Add column separator
        st.markdown('<div class="column-separator"></div>', unsafe_allow_html=True)

    with col3:
        st.markdown("<h1>Debug Information</h1>", unsafe_allow_html=True)
        
        if hasattr(st.session_state, 'prompt') and hasattr(st.session_state, 'result'):
            st.markdown("<h2>Full Prompt:</h2>", unsafe_allow_html=True)
            st.text(st.session_state.prompt)
        
            st.markdown("<h2>API Response:</h2>", unsafe_allow_html=True)
            st.json(st.session_state.result)
        
            st.markdown("<h2>Answer Explanation:</h2>", unsafe_allow_html=True)
            st.markdown('<div id="answer-explanation">', unsafe_allow_html=True)
            st.write("The model's response is parsed to determine if it contains 'yes' or 'no'.")
            st.write(f"Raw response: {st.session_state.result.get('response', '')}")
            st.write(f"Interpreted answer: {st.session_state.answer}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write("No debug information available. Run a query to see debug data.")

if __name__ == '__main__':
    main()