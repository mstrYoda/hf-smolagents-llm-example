import subprocess
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool

class WebRequestToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Website address")

class WebRequestTool(BaseTool):
    name: str = "Web Request Tool"
    description: str = (
        "This is a tool for sending a web request to a website. It return the content of the website."
    )
    args_schema: Type[BaseModel] = WebRequestToolInput

    def _run(self, argument: str) -> str:
        import requests
        response = requests.get(argument)
        return response.text
    
class WriteToFileInput(BaseModel):
    """Input schema for MyCustomTool."""
    file_name: str = Field(..., description="File name")
    content: str = Field(..., description="Content to write to file")

class WriteToFileTool(BaseTool):
    name: str = "Write to File Tool"
    description: str = (
        "This is a tool for writing given content to file."
    )
    args_schema: Type[BaseModel] = WriteToFileInput

    def _run(self, file_name: str, content: str) -> str:
        with open(file_name, "w") as f:
            out = f.write(bytearray(content))
            if out == 0:
                raise Exception("Error writing to file")
        return "Content written to file successfully"

class YFinanceToolInput(BaseModel):
    """Input for the YahooFinanceNews tool."""
    query: str = Field(description="company ticker query to look up")

tool = YahooFinanceNewsTool()

class YFinanceWrapperTool(BaseTool):
    """Tool that searches financial news on Yahoo Finance."""

    name: str = "yahoo_finance_news"
    description: str = (
        "Useful for when you need to find financial news "
        "about a public company. "
        "Input should be a company ticker. "
        "For example, AAPL for Apple, MSFT for Microsoft."
    )
    args_schema: Type[BaseModel] = YFinanceToolInput

    def _run(self, query: str) -> str:
        print(subprocess.check_output(["pip", "install", "yfinance"]))
        return tool._run(query=query)
