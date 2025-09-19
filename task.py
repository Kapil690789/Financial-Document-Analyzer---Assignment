from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor

# Creating a verification task with very explicit instructions
verification = Task(
    description=(
        "You MUST use the 'Read a file's content' tool to verify the financial document "
        "located at the path: '{file_path}'.\n"
        "Read the entire document content using the tool before proceeding.\n\n"
        "Your verification checklist is as follows:\n"
        "1. Confirm the document is readable and properly formatted.\n"
        "2. Identify the type of financial document (e.g., annual report, quarterly filing).\n"
        "3. Check for the presence of key financial statements (Income Statement, Balance Sheet, Cash Flow).\n"
        "4. Assess the document's authenticity and source credibility."
    ),
    expected_output=(
        "A detailed verification report including the document type, source, data quality, "
        "any identified issues, and a confidence level in the document's reliability."
    ),
    agent=verifier,
    async_execution=False
)

# Creating a task to analyze financial documents
analyze_financial_document = Task(
    description=(
        "Using the content of the financial document from the file path '{file_path}' "
        "and the verification report from the previous step, conduct a detailed financial analysis.\n"
        "The user's primary question is: {query}.\n\n"
        "Your analysis MUST include:\n"
        "1. A summary of the company's financial performance.\n"
        "2. Identification of key financial metrics (e.g., revenue, net income, operating margin).\n"
        "3. Analysis of trends, strengths, and weaknesses based on the data."
    ),
    expected_output=(
        "A comprehensive financial analysis report with an executive summary, "
        "detailed breakdown of key metrics, and insights addressing the user's query."
    ),
    agent=financial_analyst,
    async_execution=False,
    context=[verification]
)

# Creating an investment analysis task
investment_analysis = Task(
    description=(
        "Based on the detailed financial analysis report from the previous step, provide "
        "specific and actionable investment recommendations.\n"
        "The user's query was: {query}"
    ),
    expected_output=(
        "A clear investment recommendation (BUY, HOLD, or SELL) with a supporting thesis, "
        "rationale, and a brief risk assessment."
    ),
    agent=investment_advisor,
    async_execution=False,
    context=[analyze_financial_document]
)

# Creating a risk assessment task
risk_assessment = Task(
    description=(
        "Based on the financial document and the analysis report, conduct a comprehensive "
        "risk assessment. Focus on financial, operational, and market risks."
    ),
    expected_output=(
        "A risk assessment report detailing the key risks identified, their potential impact, "
        "and recommended mitigation strategies."
    ),
    agent=risk_assessor,
    async_execution=False,
    context=[analyze_financial_document]
)