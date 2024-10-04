import streamlit as st

st.set_page_config(page_title="LLM Systematic Review Screener", page_icon="👋",)

st.write("## LLM Systematic Review Screener! 👋")

st.markdown(
"""
This app allows you to automate Title/Abstract Screening for Systematic Reviews.

### Demo Instructions:
Page 1 
- use one of the 3 **:green-background[demo buttons]** to pull in a sample dataset of abstracts (including metadata e.g. title, abstract, doi, authors, etc.)
- wait for gpt-4o-mini to complete structured data extraction and article screening of each article based on predefined research question and exclusion criteria
- optionally download generated file with extracted data and LLM screening decision

Page 2
- load downloaded data from Page 1, or press the "Use Results from Step 1" button to load in data set
- for each abstract:
--> the left side of the page shows structured data extracted by the LLM, with buttons that highlight the relevant passages in the original abstract that it was extracted from
--> the right side of the page shows the original abstract
- manual screening can be done now
- when finished, you may download the final results containing human and LLM screening decision

Benefits
- Decreasing title/abstract screening requirements from 2 human reviewers to 1 human + LLM - speed + accessibility
- LLM highlighted abstracts provide visual guidance to relevant parts of the abstract, for humans to quickly make inclusion/exclusion decisions
- Python.
"""
)