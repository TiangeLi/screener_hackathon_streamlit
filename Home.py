import streamlit as st

st.set_page_config(page_title="LLM Systematic Review Screener", page_icon="👋",)

st.write("## LLM Systematic Review Screener! 👋")

st.markdown(
"""
This app allows you to automate Title/Abstract Screening for Systematic Reviews.

### How it works

**Page 1 - LLM Screener**:
- Upload a CSV file with Title/Abstracts to screen
- Enter a screening question and exclusion criteria
- Click "Screen"
- Download the results!

**Page 2 - Human Screening**:
- Review each abstract, with LLM generated highlights to quickly zero in on relevant information
- Mark the abstracts that should be excluded
- Download the results!
"""
)