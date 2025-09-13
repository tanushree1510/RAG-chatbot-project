import streamlit as st
import requests

# --- Streamlit Page Config ---
st.set_page_config(page_title="BGSCET College RAG Chatbot", page_icon="🎓", layout="centered")

# --- Custom Dark Theme Styling ---
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #ffffff;
        border-radius: 10px;
        border: 1px solid #4f4f4f;
        padding: 10px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-size: 16px;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.05);
        transition: all 0.2s ease-in-out;
    }
    .answer-box {
        background-color: #1c1e24;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        border: 1px solid #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- UI Content ---
st.markdown("<h1 style='text-align: center;'>🎓 BGSCET College RAG Chatbot</h1>", unsafe_allow_html=True)
st.write("Ask anything about your college, and I will fetch the answer from the knowledge base.")

question = st.text_input("Enter your question:")

if st.button("🔍 Get Answer"):
    if question.strip():
        with st.spinner("Fetching answer..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/query",
                    json={"question": question}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.markdown(
                        f"<div class='answer-box'><b>Answer:</b><br>{data['answer']}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.error("⚠️ API error: Check if the backend server is running.")
            except Exception as e:
                st.error(f"❌ Could not connect to API. Error: {e}")
    else:
        st.warning("Please enter a question before submitting.")
