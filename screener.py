from dotenv import load_dotenv
load_dotenv(override=True)
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from typing import TypedDict, Optional

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

screening_prompt = \
"""Given the following article information, please decide if it should be included in the analysis, based on the screening question and exclusion criteria.

<article>
{article}
</article>

<screening_question>
{screening_question}
</screening_question>

<exclusion_criteria>
{exclusion_criteria}
</exclusion_criteria>"""

sr_prompt = ChatPromptTemplate([
    ("system", screening_prompt),
])

class Inclusion(TypedDict):
    include: bool
    reason_if_excluded: Optional[str]

screener_chain = sr_prompt | llm.with_structured_output(Inclusion, method="json_schema", strict=True)