from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from typing_extensions import TypedDict, Optional


class ExtractedSources(TypedDict):
    data_sources: Optional[list[int]]
    study_design: Optional[list[int]]
    study_accrural_periods: Optional[list[int]]
    sample_size: Optional[list[int]]
    exposures: Optional[list[int]]
    exposure_ascertainment: Optional[list[int]]
    outcomes: Optional[list[int]]
    outcome_ascertainment: Optional[list[int]]
    all_results: Optional[list[int]]
    conclusions: Optional[list[int]]


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

template = \
"""Given the following article AND extracted data, your task is to return a list of sentence indices that each category of data is sourced from.
For each category, you may find that the data is not available, or that it is available in multiple sentences.
You may return an empty list, a single index, or multiple indices. The indices do not have to be contiguous, since information may be spread across multiple sentences.

<article>
{article}
</article>

<extracted_data>
{extracted_data}
</extracted_data>"""

prompt = ChatPromptTemplate([
    ("system", template),
])

get_sources_chain = prompt | llm.with_structured_output(ExtractedSources, method="json_schema", strict=True)