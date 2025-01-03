from typing import Optional
from smolagents import CodeAgent, tool, LiteLLMModel, ToolCallingAgent

@tool
def send_request(addr: str) -> str:
    """Sends http get request to the given address and returns the response
    
    Args:
        addr: The address to send the request to
    """
    import requests
    response = requests.get(addr)
    return response.text

model = LiteLLMModel(
    model_id="ollama/qwen2.5-coder:latest",
    api_base="http://localhost:11434"
)

@tool
def create_file(name: str, content: bytearray) -> Exception:
    """Creates a file with given name with the given content
    
    Args:
        name: The name of the file
        content: The content of the file as a bytearray
    """
    #create file if not exists and handle already exist error
    with open(name, "wb") as f:
        out = f.write(content)
        if out == 0:
            raise Exception("Error writing to file")
    return None

agent = CodeAgent(tools=[send_request, create_file], model=model, additional_authorized_imports=["datetime"])
#agent = ToolCallingAgent(tools=[request], model=model)

#print(agent.run("Give me a code block that finds articles about Golang or Machine Learning from https://dev.to/feed"))
print(agent.run("Get the content of the website dev.to/feed and write it to file named dev_feed.txt"))
