from pydantic import BaseModel, Field
from autogen_ext.tools.langchain import LangChainToolAdapter
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import StructuredTool

search = DuckDuckGoSearchRun()
search.args_schema.model_rebuild()

class SearchInput(BaseModel):
    query: str = Field(..., description="The search query to run")

def search_function(query: str) -> str:
    return search.invoke(query)

def build_search_tool() -> LangChainToolAdapter:
    langchain_searcher = StructuredTool.from_function(
        func=search_function,
        name="internet_search",
        description="Search the internet using DuckDuckGo",
        args_schema=SearchInput,
        strict=True,
    )
    return LangChainToolAdapter(langchain_searcher)