# Import the decorator from the main 'crewai' library's submodule
from crewai.tools import tool

# Import the pre-built tools that we know are working
from crewai_tools import FileReadTool

# Import the DuckDuckGo library directly
from duckduckgo_search import DDGS

# --- DEFINE YOUR CUSTOM TOOLS HERE ---

# 1. Document Reading Tool (from crewai_tools)
financial_document_tool = FileReadTool()

# 2. Custom Web Search Tool (our own stable version)
@tool("Web Search Tool")
def search_tool(query: str) -> str:
    """
    A custom tool to search the web using DuckDuckGo.
    This is more stable than importing from crewai_tools.
    """
    print(f"Searching the web for: {query}")
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=5)]
    return "\n".join(str(res) for res in results) if results else "No results found."

# 3. Placeholder Investment Analysis Tool
@tool("Investment Analysis Tool")
def investment_analysis_tool(query: str) -> str:
    """
    A placeholder tool for investment analysis.
    """
    return f"Investment analysis for '{query}' has been noted and will be incorporated."

# 4. Placeholder Risk Assessment Tool
@tool("Risk Assessment Tool")
def risk_assessment_tool(query: str) -> str:
    """
    A placeholder tool for risk assessment.
    """
    return f"Risk assessment for '{query}' has been noted and will be incorporated."