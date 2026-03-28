import streamlit as st
import os
from chat import retrieval_chain

# --- Page Configuration ---
st.set_page_config(
    page_title="Gillmore AI", 
    page_icon="wbs.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Advanced Professional Styling (CSS) ---
st.markdown("""
    <style>
    /* Global Background and Font */
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Inter', sans-serif;
    }
    /* Sidebar Styling - WBS Deep Blue */
    section[data-testid="stSidebar"] {
        background-color: #09baeb !important;
    }
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] p {
        color: black !important;
    }
    /* FIX: Sidebar Button Visibility */
    div.stButton > button {
        width: 100%;
        background-color: transparent;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 8px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: white !important;
        color: #002147 !important;
        border: 1px solid white;
    }
    /* Chat Avatar Logic - Fix for Scaling */
    [data-testid="stChatMessageAvatarCustom"] {
        width: 40px !important;
        height: 40px !important;
        border-radius: 50%;
        border: 1px solid #e0e0e0;
        object-fit: contain; /* Ensures logo isn't stretched */
        background-color: white;
    }
    /* Prompt Pills Styling */
    .pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 10px;
    }
    
    /* Header Polish */
    .app-header {
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar & Branding ---
with st.sidebar:
    if os.path.exists("wbs.png"):
        # We use a container to keep the logo crisp and proportional
        st.image("wbs.png", width="stretch")
    
    st.markdown("---")
    st.info("""
        **Expert Research Assistant** *Gillmore Centre for Financial Technology* Warwick Business School
    """)
    
    st.divider()
    # Visible and styled Clear Button
    if st.button("🗑️ Clear Conversation"):
        st.session_state.conversation = []
        st.rerun()

    st.divider()
    st.caption("Developed by FutureFinance.AI")

# --- Main UI Layout ---
st.markdown('<div class="app-header">', unsafe_allow_html=True)
st.title("🤖 Gillmore AI")
st.markdown("*An AI-powered portal into Gillmore Centre's research and financial innovation.*")
st.markdown('</div>', unsafe_allow_html=True)

# Initialize Session State
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# --- Welcome Screen & Interactive Prompt Starters ---
if not st.session_state.conversation:
    st.markdown("### How can I help you today?")
    st.write("Select a research theme to start, or type your own question below.")
    
    # Interactive Pills (Clicking these sets the chat input)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📑 Latest Research Paper Info"):
            st.session_state.pending_query = "What is the latest research paper by Gillmore Academics? Give a brief summary of the same."
    with col2:
        if st.button("🤖 Introduce Gillmore AI"):
            st.session_state.pending_query = "Can you introduce yourself to someone who new?"

# --- Chat Display ---
for entry in st.session_state.conversation:
    with st.chat_message("user", avatar="👤"):
        st.markdown(entry['user'])
    # Using wbs.png for AI avatar
    with st.chat_message("assistant", avatar="wbs.png"):
        st.markdown(entry['assistant'])

# --- Chat Input Logic ---
# Handle clicks from prompt pills
if "pending_query" in st.session_state:
    user_input = st.session_state.pending_query
    del st.session_state.pending_query # Clear it so it doesn't trigger again
else:
    user_input = st.chat_input("Ask a question about Gillmore research...")

if user_input:
    # 1. Store and display user message
    st.session_state.conversation.append({"user": user_input, "assistant": ""})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # 2. Generate AI Response
    with st.chat_message("assistant", avatar="wbs.png"):
        with st.spinner("Consulting Research Database..."):
            try:
                response = retrieval_chain.invoke({"input": user_input})
                answer = response["answer"]
            except Exception as e:
                answer = "⚠️ System Error: Unable to access the research database. Please verify API configuration."
            
            st.session_state.conversation[-1]["assistant"] = answer
            st.markdown(answer)