import streamlit as st

st.set_page_config(page_title="LLM Systematic Review Screener", page_icon="🧊", layout="wide")

st.write("## LLM Systematic Review Screener! 👋")
st.write("This app allows you to automate Title/Abstract Screening for Systematic Reviews.")

'---'

col1, col2 = st.columns(2)

left = """### Motivation

Systematic reviews are a cornerstone of evidence based medicine, but generating them is:
- slow
- tedious
- expensive
- unsustainable

We propose automating the Title/Abstract screening component of systematic review generation.
This step is typically done with 2 human reviewers (for interrater reliability and concordance), taking weeks of human labor per reviewer.
Now we can change it to 1 human + 1 LLM!"""

right = """### Demo Instructions:
Page 1 
- use one of the 3 **:green-background[demo buttons]** to pull in a sample dataset of abstracts (including metadata e.g. title, abstract, doi, authors, etc.)
- wait for gpt-4o-mini to complete structured data extraction and article screening of each article based on predefined research question and exclusion criteria
- optionally download generated file with extracted data and LLM screening decision

Page 2
- load downloaded data from Page 1, or press the "Use Results from Step 1" button to load in data set
- for each abstract: the left side shows structured data extracted by the LLM; the right shows the original abstract for human screening.
- contextual :blue-background[highlighting] of the abstract can be done by clicking on the structured data fields to highlight the source text in the abstract
- manual screening can be done now
- when finished, you may download the final results containing human and LLM screening decision

Benefits
- Decreasing title/abstract screening requirements from 2 human reviewers to 1 human + LLM - speed + accessibility
- LLM highlighted abstracts provide visual guidance to relevant parts of the abstract, for humans to quickly make inclusion/exclusion decisions
- Python."""

with col1:
    st.markdown(left)
    
with col2:
    st.markdown(right)