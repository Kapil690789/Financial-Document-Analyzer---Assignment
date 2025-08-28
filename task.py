import os
from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, financial_document_tool, investment_analysis_tool, risk_assessment_tool

# Creating a task to analyze financial documents
analyze_financial_document = Task(
    description="""
    Analyze the financial document based on the user's query: {query}
    
    Steps to follow:
    1. Read and extract content from the financial document using the document reading tool
    2. Verify the document contains relevant financial information
    3. Identify key financial metrics, ratios, and performance indicators
    4. Analyze trends, strengths, and areas of concern
    5. Research current market conditions that may impact the analysis
    6. Provide comprehensive insights addressing the user's specific query
    
    Focus on providing accurate, data-driven analysis with proper context and explanations.
    """,
    expected_output="""
    A comprehensive financial analysis report including:
    - Executive summary of key findings
    - Detailed analysis of financial metrics and performance
    - Market context and industry comparisons where relevant
    - Key strengths and areas of concern identified
    - Specific insights addressing the user's query
    - Professional recommendations based on the analysis
    
    The report should be well-structured, professional, and based on actual data from the document.
    """,
    agent=financial_analyst,
    tools=[financial_document_tool, search_tool],
    async_execution=False,
)

# Creating an investment analysis task
investment_analysis = Task(
    description="""
    Based on the financial document analysis, provide specific investment recommendations.
    
    User query: {query}
    
    Steps:
    1. Review the financial analysis results
    2. Assess investment potential based on financial health and performance
    3. Consider current market conditions and industry trends
    4. Evaluate risk-return profile
    5. Develop specific, actionable investment recommendations
    6. Provide rationale for each recommendation
    """,
    expected_output="""
    Investment recommendation report containing:
    - Investment thesis and rationale
    - Specific investment recommendations (buy/hold/sell with target prices if applicable)
    - Risk assessment and mitigation strategies
    - Time horizon and expected returns
    - Key factors to monitor going forward
    - Regulatory and compliance considerations
    
    All recommendations should be based on solid financial analysis and include appropriate risk disclosures.
    """,
    agent=investment_advisor,
    tools=[investment_analysis_tool, search_tool],
    async_execution=False,
)

# Creating a risk assessment task
risk_assessment = Task(
    description="""
    Conduct a comprehensive risk assessment based on the financial document and analysis.
    
    User query: {query}
    
    Focus areas:
    1. Financial risks (credit, liquidity, market risk)
    2. Operational risks
    3. Industry and competitive risks
    4. Regulatory and compliance risks
    5. Macroeconomic risks
    6. Risk mitigation recommendations
    """,
    expected_output="""
    Risk assessment report including:
    - Risk profile summary (low/medium/high risk categories)
    - Detailed analysis of identified risks
    - Quantitative risk metrics where available
    - Risk mitigation strategies and recommendations
    - Stress testing scenarios and potential impacts
    - Monitoring and early warning indicators
    - Compliance and regulatory risk considerations
    
    The assessment should be thorough, practical, and actionable for decision-making.
    """,
    agent=risk_assessor,
    tools=[risk_assessment_tool, search_tool],
    async_execution=False,
)

# Creating a verification task
verification = Task(
    description="""
    Verify the financial document quality and completeness before analysis.
    
    Verification checklist:
    1. Confirm the document is readable and properly formatted
    2. Identify the type of financial document (annual report, quarterly filing, etc.)
    3. Check for completeness of key financial statements
    4. Verify data consistency and identify any anomalies
    5. Assess document authenticity and source credibility
    6. Flag any missing information that could impact analysis
    """,
    expected_output="""
    Document verification report containing:
    - Document type and source identification
    - Completeness assessment of financial data
    - Data quality and consistency evaluation
    - Any identified issues or limitations
    - Recommendations for proceeding with analysis
    - Confidence level in the document's reliability
    
    The verification should ensure the document is suitable for comprehensive financial analysis.
    """,
    agent=verifier,
    tools=[financial_document_tool],
    async_execution=False
)
