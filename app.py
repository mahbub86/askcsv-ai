import streamlit as st
from agent import agent
from tools.csv_tools import load_csv, analyze_csv
from plotly.graph_objs import Figure
import pandas as pd
import time

# -------- Page Config -------- #
st.set_page_config(page_title="AskCSV AI", layout="wide", page_icon="📊")

# -------- Session State -------- #
if "query_history" not in st.session_state:
    st.session_state.query_history = []

# -------- Custom Style -------- #
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(135deg, #fdfbfb, #ebedee, #e0f7fa);
        background-attachment: fixed;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    .stButton button {
        background: linear-gradient(to right, #36D1DC, #5B86E5, #a06cd5);
        color: white;
        padding: 0.2em 1em;
        border-radius: 10px;
        font-size: 30px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: scale(1.03);
        background: linear-gradient(to right, #5B86E5, #a06cd5, #f093fb);
    }
</style>
""", unsafe_allow_html=True)

# -------- Sidebar -------- #
with st.sidebar:
    st.markdown("## 📂 Upload CSV")
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    
    if uploaded_file:
        load_csv(uploaded_file)
        st.success("✅ CSV loaded")

    st.markdown("---")
    st.markdown("### 💬 Query History")
    if st.session_state.query_history:
        for i, q in enumerate(reversed(st.session_state.query_history[-10:])):
            st.markdown(f"- {q}")
        if st.button("🧹 Clear History"):
            st.session_state.query_history.clear()
            st.rerun()  # ✅ updated
    else:
        st.info("No queries yet.")

# -------- Main Title -------- #
st.markdown("""
<h1 style='text-align: center; font-size: 3em; color: #333;'>📊 AskCSV AI</h1>
<p style='text-align: center; color: #666;'>Upload your CSV and ask anything from it!</p>
<hr style='border: none; height: 2px; background: linear-gradient(to right, #36D1DC, #5B86E5, #a06cd5); margin-top: 1rem;'>
""", unsafe_allow_html=True)

# -------- Main Input -------- #
if uploaded_file:
    query = st.text_input("🔍 Ask your question")

    if st.button("🚀 Ask"):
        with st.spinner("🧠 Thinking..."):
            st.session_state.query_history.append(query)

            response = analyze_csv(query)

            st.markdown("### 📊 Result")

            if isinstance(response, Figure):
                st.plotly_chart(response, use_container_width=True)
            elif "scattermapbox" in str(type(response)).lower():
                st.plotly_chart(response, use_container_width=True)
            elif hasattr(response, "to_markdown"):
                st.markdown(response.to_markdown(), unsafe_allow_html=True)
            elif isinstance(response, str):
                st.markdown(response)
            else:
                llm_response = agent.run(query)
                st.markdown("### 🤖 LLM Response:")
                st.write(llm_response)
