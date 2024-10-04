from dotenv import load_dotenv
load_dotenv(override=True)

import nltk
from nltk.tokenize import sent_tokenize
from tagging import get_sources_chain
import streamlit as st
import pandas as pd

nltk.download('punkt')

st.set_page_config(layout="wide")

if "screening_items" not in st.session_state:
    st.session_state.screening_items = []
if "current_item_index" not in st.session_state:
    st.session_state.current_item_index = 0
if "tagged_indices" not in st.session_state:
    st.session_state.tagged_indices = []
if "tagged_data" not in st.session_state:
    st.session_state.tagged_data = {}

if "screening_results" not in st.session_state:
    st.session_state.screening_results = []

with st.sidebar:
    file = st.file_uploader("Upload LLM Screening Results", type="csv")
    '---'
    if st.button("Use Results from Step 1"):
        file = "example_data/llm_screening_results.csv"
        st.session_state.current_item_index = 0
        st.session_state.screening_results = []
    if file:
        file = pd.read_csv(file)
        st.session_state.screening_items = [{
            "sentences": sent_tokenize(row["original_text"]),
            "include": row["include"],
            "extracted_data": {
                "data_sources": row["data_sources"],
                "study_design": row["study_design"],
                "study_accrural_periods": row["study_accrural_periods"],
                "sample_size": row["sample_size"],
                "exposures": row["exposures"],
                "exposure_ascertainment": row["exposure_ascertainment"],
                "outcomes": row["outcomes"],
                "outcome_ascertainment": row["outcome_ascertainment"],
                "all_results": row["all_results"],
                "conclusions": row["conclusions"],
            }
        } for _, row in file.iterrows()]
    '---'
    st.write(f"## :green[**{st.session_state.current_item_index} / {len(st.session_state.screening_items)} articles screened**]")


with st.expander("Show Human / LLM Screening Concordance"):
    compare_df = [
        {"Article": sent_tokenize(entry["original_text"])[0],  # hacky + inefficient but oh well
        "Human Decision": entry["human_include"], 
        "LLM Decision": entry["llm_include"],
        "Concordant": entry["llm_include"] == entry["human_include"]}
    for entry in st.session_state.screening_results]
    st.write(pd.DataFrame(compare_df))

'---'

coll, colr = st.columns(2)

if not st.session_state.screening_items:
    st.write("No articles to screen. Please upload a CSV file with the LLM screening results.")

elif st.session_state.current_item_index >= len(st.session_state.screening_items):
    st.write("Finished screening all articles!")
    csv = pd.DataFrame(st.session_state.screening_results)
    export = csv.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download screening results", 
        data=export,
        file_name="final_screening_results.csv",
        mime="text/csv"
    )

else:
    if st.session_state.screening_items:
        if not st.session_state.tagged_data:
            curr_item = st.session_state.screening_items[st.session_state.current_item_index]
            tagged_article = " ".join([f"<sentence #{i}>{sentence}</sentence #{i}>" for i, sentence in enumerate(curr_item["sentences"])])
            with st.spinner("LLM tagging data sources..."):
                st.session_state.tagged_data = get_sources_chain.invoke(
                    {
                        "article": tagged_article,
                        "extracted_data": curr_item["extracted_data"],
                    }
                )

        curr_item = st.session_state.screening_items[st.session_state.current_item_index]

        with colr:
            text = ''
            for i, sentence in enumerate(curr_item["sentences"]):
                if i not in st.session_state.tagged_indices:
                    text += f"{sentence} "
                else:
                    text += f":blue-background[{sentence}] "
                if i == 0:
                    text += "\n\n"
            st.write("**Original Abstract:**\n\n")
            st.write(text)
            _ic1, _ic2 = st.columns(2)
            with _ic1:
                if st.button("Include", use_container_width=True):
                    result = {"llm_include": curr_item["include"], "human_include": True, **curr_item["extracted_data"], "original_text": " ".join(curr_item["sentences"])}
                    st.session_state.tagged_indices = []
                    st.session_state.tagged_data = {}
                    st.session_state.current_item_index += 1
                    st.session_state.screening_results.append(result)
                    st.rerun()
            with _ic2:
                if st.button("Exclude", use_container_width=True):
                    result = {"llm_include": curr_item["include"], "human_include": False, **curr_item["extracted_data"], "original_text": " ".join(curr_item["sentences"])}
                    st.session_state.tagged_indices = []
                    st.session_state.tagged_data = {}
                    st.session_state.current_item_index += 1
                    st.session_state.screening_results.append(result)
                    st.rerun()
        with coll:
            for selection in curr_item["extracted_data"]:
                _c1, _c2 = st.columns((2, 3))
                with _c1:
                    if st.button(f"Highlight :blue[{selection.replace('_', ' ').title()}]", use_container_width=True):
                        st.session_state.tagged_indices = st.session_state.tagged_data[selection]
                        st.rerun()
                with _c2:
                    st.caption(curr_item["extracted_data"][selection])
