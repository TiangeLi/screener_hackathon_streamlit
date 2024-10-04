import streamlit as st
import pandas as pd

from extractor import extractor_chain
from screener import screener_chain

default_screening_question = "What is the association between exposure to radiotherapy for prostate cancer and incidence/risk of second malignancy / second primary cancers?"
default_exclusion_criteria = "non-clinical studies, editorials, review articles, case reports, conference abstracts, basic science papers, unclear comparator group, metastatic tumors, non-standard treatment for prostate cancer (such as cryotherapy), articles not dealing with radiation induced malignancy"

st.set_page_config(page_title="Oct 4 2024 Hackathon - Systematic Review Screener", layout="wide")

if "articles" not in st.session_state:
    st.session_state.articles = []
if "screening_question" not in st.session_state:
    st.session_state.screening_question = ""
if "exclusion_criteria" not in st.session_state:
    st.session_state.exclusion_criteria = ""
if "final_output" not in st.session_state:
    st.session_state.final_output = []


LIMIT_LINES = 200
EXTRACTOR_BATCH_SIZE = 100
# save on api costs, so limit to 200 lines for now

with st.sidebar:
    file = st.file_uploader("Upload a CSV file containing the articles to screen", type="csv")
    '---'
    if st.button("Use Sample Random Dataset", use_container_width=True):
        file = "example_data/example_random_set.csv"
        st.session_state.screening_question = default_screening_question
        st.session_state.exclusion_criteria = default_exclusion_criteria
    if st.button("Use Sample Validated Dataset", use_container_width=True):
        file = "example_data/example_validation_set.csv"
        st.session_state.screening_question = default_screening_question
        st.session_state.exclusion_criteria = default_exclusion_criteria
    if st.button("Use Sample Tiny Set", use_container_width=True):
        file = "example_data/example_tiny_set.csv"
        st.session_state.screening_question = default_screening_question
        st.session_state.exclusion_criteria = default_exclusion_criteria
    if file: 
        dataset = pd.read_csv(file)[:LIMIT_LINES]
        articles = [f"Title: {row['Title']}\nAbstract: {row['Abstract']}" for _, row in dataset.iterrows()]
        st.session_state.articles = articles
        length = len(st.session_state.articles)
        st.write(f"Number of articles to screen: {length}")

col1, col2 = st.columns(2)

with col1:
    st.write("Screening Questions")
    st.session_state.screening_question = st.text_area("Enter the screening question", value=st.session_state.screening_question)

with col2:
    st.write("Exclusion Criteria")
    st.session_state.exclusion_criteria = st.text_area("Enter the exclusion criteria", value=st.session_state.exclusion_criteria)


if st.button("Extract Data"):
    info = st.empty()
    download = st.empty()
    data_container = st.empty()
    inc_cnt, exc_cnt = 0, 0
    st.session_state.final_output = []
    with st.spinner(f"Extracting and screening [{len(st.session_state.articles)}] articles..."):
        batch_size = EXTRACTOR_BATCH_SIZE
        for i in range(0, len(st.session_state.articles), batch_size):
            batch = st.session_state.articles[i:i+batch_size]
            to_extract = [{"article": article, "screening_question": st.session_state.screening_question} for article in batch]
            extracted = extractor_chain.batch(to_extract)
            to_screen = [{"article": article, "screening_question": st.session_state.screening_question, "exclusion_criteria": st.session_state.exclusion_criteria} for article in extracted]
            screened = screener_chain.batch(to_screen)

            inc_cnt += len([s for s in screened if s["include"]])
            exc_cnt += len([s for s in screened if not s["include"]])
            
            final = [{**article, "include": s["include"], "original_text": original} for article, s, original in zip(extracted, screened, batch)]
            st.session_state.final_output.extend(final)
            info.markdown(f"### Screened **{inc_cnt + exc_cnt}** articles.\n\nIncluded: **{inc_cnt}**  \nExcluded: **{exc_cnt}**")
            if st.session_state.final_output:
                csv = pd.DataFrame(st.session_state.final_output)
                export = csv.to_csv(index=False).encode('utf-8')
                with open("example_data/llm_screening_results.csv", "wb") as f:
                    f.write(export)
                download.download_button(
                    label=':red[Download llm_screening_results.csv]',
                    data=export,
                    file_name='llm_screening_results.csv',
                    mime='text/csv'
                )
            with data_container.expander(f"View last {min(20, len(final))} extracted articles"):
                for article in final[-20:]:
                    st.write(article)