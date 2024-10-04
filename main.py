import streamlit as st
import pandas as pd

from extractor import extractor_chain
from screener import screener_chain

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
# save on api costs, so limit to 200 lines for now


with st.sidebar:
    file = st.file_uploader("Upload a CSV file containing the articles to screen", type="csv")
    if file: 
        dataset = pd.read_csv(file)[:LIMIT_LINES]
        articles = [f"Title: {row['Title']}\nAbstract: {row['Abstract']}" for _, row in dataset.iterrows()]
        st.session_state.articles = articles
        length = len(st.session_state.articles)
        st.write(f"Number of articles to screen: {length}")
    if st.session_state.final_output:
        '---'
        csv = pd.DataFrame(st.session_state.final_output)
        export = csv.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=':red[Download results]',
            data=export,
            file_name='results.csv',
            mime='text/csv'
        )

col1, col2 = st.columns(2)

with col1:
    st.write("Screening Questions")
    st.session_state.screening_question = st.text_area("Enter the screening question")

with col2:
    st.write("Exclusion Criteria")
    st.session_state.exclusion_criteria = st.text_area("Enter the exclusion criteria")


if st.button("Extract Data"):
    info = st.empty()
    inc_cnt, exc_cnt = 0, 0
    with st.spinner("Extracting data..."):
        batch_size = 100
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
            info.markdown(f"### Screened {inc_cnt + exc_cnt} articles. {inc_cnt} included and {exc_cnt} excluded.")
            with st.expander("View last 20 extracted articles"):
                for article in final[-20:]:
                    st.write(article)