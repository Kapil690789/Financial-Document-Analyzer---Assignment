import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import BaseTool
from crewai_tools.tools.serper_dev_tool import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader
import asyncio
from typing import Type
from pydantic import BaseModel, Field

# Creating search tool
search_tool = SerperDevTool()

class FinancialDocumentToolInput(BaseModel):
    """Input schema for FinancialDocumentTool."""
    path: str = Field(..., description="Path of the PDF file to read")

class FinancialDocumentTool(BaseTool):
    name: str = "read_financial_document"
    description: str = "Tool to read and extract text content from PDF financial documents"
    args_schema: Type[BaseModel] = FinancialDocumentToolInput

    def _run(self, path: str = 'data/sample.pdf') -> str:
        """Tool to read data from a pdf file from a path

        Args:
            path (str): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Financial Document content
        """
        try:
            if not os.path.exists(path):
                return f"Error: File {path} does not exist"
            
            loader = PyPDFLoader(path)
            docs = loader.load()

            full_report = ""
            for doc in docs:
                content = doc.page_content
                
                # Clean and format the financial document data
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                    
                full_report += content + "\n"
                
            return full_report if full_report.strip() else "No content found in the PDF file"
            
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

# Creating Investment Analysis Tool
class InvestmentAnalysisToolInput(BaseModel):
    """Input schema for InvestmentAnalysisTool."""
    financial_data: str = Field(..., description="Financial document data to analyze")

class InvestmentAnalysisTool(BaseTool):
    name: str = "analyze_investment"
    description: str = "Tool to analyze financial data and provide investment insights"
    args_schema: Type[BaseModel] = InvestmentAnalysisToolInput

    def _run(self, financial_data: str) -> str:
        """Analyze financial document data for investment insights"""
        try:
            # Clean up the data format
            processed_data = financial_data.strip()
            processed_data = ' '.join(processed_data.split())  # Remove extra whitespaces
            
            if not processed_data:
                return "No financial data provided for analysis"
            
            # Basic analysis framework
            analysis_points = []
            
            # Look for key financial indicators
            if any(term in processed_data.lower() for term in ['revenue', 'income', 'profit', 'earnings']):
                analysis_points.append("Revenue and profitability metrics identified")
            
            if any(term in processed_data.lower() for term in ['debt', 'liability', 'loan']):
                analysis_points.append("Debt and liability information found")
                
            if any(term in processed_data.lower() for term in ['cash', 'assets', 'equity']):
                analysis_points.append("Asset and cash position data available")
            
            return f"Investment Analysis Summary:\n" + "\n".join(f"- {point}" for point in analysis_points) if analysis_points else "Basic financial document structure identified"
            
        except Exception as e:
            return f"Error in investment analysis: {str(e)}"

# Creating Risk Assessment Tool
class RiskAssessmentToolInput(BaseModel):
    """Input schema for RiskAssessmentTool."""
    financial_data: str = Field(..., description="Financial document data to assess for risks")

class RiskAssessmentTool(BaseTool):
    name: str = "assess_risk"
    description: str = "Tool to assess financial risks from document data"
    args_schema: Type[BaseModel] = RiskAssessmentToolInput

    def _run(self, financial_data: str) -> str:
        """Create risk assessment from financial document data"""
        try:
            processed_data = financial_data.strip()
            
            if not processed_data:
                return "No financial data provided for risk assessment"
            
            risk_factors = []
            
            # Identify potential risk indicators
            if any(term in processed_data.lower() for term in ['loss', 'deficit', 'decline', 'decrease']):
                risk_factors.append("Potential negative financial trends identified")
            
            if any(term in processed_data.lower() for term in ['debt', 'liability', 'obligation']):
                risk_factors.append("Debt obligations require monitoring")
                
            if any(term in processed_data.lower() for term in ['volatile', 'uncertain', 'risk', 'challenge']):
                risk_factors.append("Market volatility or uncertainty mentioned")
            
            return f"Risk Assessment Summary:\n" + "\n".join(f"- {factor}" for factor in risk_factors) if risk_factors else "Standard financial risk monitoring recommended"
            
        except Exception as e:
            return f"Error in risk assessment: {str(e)}"

# Create tool instances
financial_document_tool = FinancialDocumentTool()
investment_analysis_tool = InvestmentAnalysisTool()
risk_assessment_tool = RiskAssessmentTool()
