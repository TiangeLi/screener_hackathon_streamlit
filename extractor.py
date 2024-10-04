from dotenv import load_dotenv
load_dotenv(override=True)
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from typing import TypedDict, Annotated, Literal, Optional

class ExtractedStudyData(TypedDict):
    data_sources: Annotated[Optional[str], ..., "for each data collected, summarize what/where/when/who it was collected from"]
    study_design: Annotated[Optional[Literal["Cohort", "Case-control", "Cross-sectional", "", "Experimental", "Other"]], ..., "based on the data source, what is the type of study conducted?"]
    study_accrural_periods: Optional[str]
    sample_size: Optional[int]
    exposures: Annotated[Optional[str], ..., "exposures, with the sources of the exposures if available"]
    exposure_ascertainment: Annotated[Optional[str], ..., "i.e., how was the exposure measured / what was the data source?"]
    outcomes: Optional[str]
    outcome_ascertainment: Annotated[Optional[str], ..., "i.e., how was the outcome measured / what was the data source?"]
    all_results: Annotated[Optional[str], ..., "results verbatim, including all stats and metrics where available"]
    conclusions: Optional[str]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

template = \
"""Please very carefully extract the following data from the article. 
Be very meticulous and specific for each category. If information is not available for a category, please leave it blank.

If possible, please extract data as it relates to this question of interest. Please pay attention to the screening question to inform your extraction.
<screening_question>
{screening_question}
</screening_question>

<article>
{article}
</article>"""

prompt = ChatPromptTemplate([
    ("system", template),
])

extractor_chain = prompt | llm.with_structured_output(ExtractedStudyData, method="json_schema", strict=True)