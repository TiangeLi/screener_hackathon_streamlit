import streamlit as st
import pandas as pd

from dotenv import load_dotenv
load_dotenv(override=True)

from screening import get_sources_chain

from nltk.tokenize import sent_tokenize

file = pd.read_csv("llm_extractor_output.csv")

if "tagged_indices" not in st.session_state:
    st.session_state.tagged_indices = []



items = [{
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


if "tagged_data" not in st.session_state:
    st.session_state.tagged_data = get_sources_chain.invoke(
        {
            "article": " ".join([f"<{i}>{sentence}</{i}>" for i, sentence in enumerate(items[0]["sentences"])]),
            "extracted_data": items[0]["extracted_data"],
        }
    )



text = ''
for i, sentence in enumerate(items[0]["sentences"]):
    if i not in st.session_state.tagged_indices:
        text += f"{sentence} "
    else:
        text += f":blue-background[{sentence}] "
    
st.write(text)

for selection in items[0]["extracted_data"]:
    if st.button(selection):
        st.session_state.tagged_indices = st.session_state.tagged_data[selection]
        st.rerun()

