from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolExecutor


def get_tool_belt():
    return [
        ArxivQueryRun(),
        DuckDuckGoSearchRun()
    ]


def get_function_calling_model():
    functions = [convert_to_openai_function(t) for t in get_tool_belt()]

    model_with_tools = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    model_with_tools = model_with_tools.bind_functions(functions)
    return model_with_tools


def get_tool_executor():
    return ToolExecutor(get_tool_belt())
