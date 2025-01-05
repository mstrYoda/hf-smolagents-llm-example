from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector, SearchType
from phi.embedder.ollama import OllamaEmbedder

def send_request(addr: str) -> str:
    """Sends http get request to the given address and returns the response
    
    Args:
        addr: The address to send the request to

    Returns:
        str: The response text
    """
    import requests
    response = requests.get(addr)
    return response.text

def write_to_file(file_name: str, content: str) -> Exception:
    """Write the given string content to the file with given file_name
    
    Args:
        file_name: The name of the file
        content: The content of the file as a string
    """
    with open(file_name, "w") as f:
        out = f.write(content)
        if out == 0:
            raise Exception("Error writing to file")
    return None

embedder = OllamaEmbedder()

gemini_model = Gemini(id="gemini-2.0-flash-exp", api_key="")

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://www.golang-book.com/public/pdf/gobook.pdf"],
    vector_db=PgVector(table_name="programming", 
                       db_url=db_url, 
                       search_type=SearchType.hybrid, 
                       embedder=embedder),
)
# Load the knowledge base: Comment out after first run
#knowledge_base.load(recreate=True, upsert=True)

web_agent = Agent(
    model=gemini_model,
    knowledge_base=knowledge_base,
    description="You are a helper agent that searches knowledge base for the requested content",
    instructions=[
        "For the requested content, using the knowledge_base to answer the question",],
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
    debug_mode=True,
)

web_agent.print_response(
    """Generate me an example code about writing data to file with Go""", 
                         stream=False, 
                         show_message=True, 
                         show_reasoning=True)
