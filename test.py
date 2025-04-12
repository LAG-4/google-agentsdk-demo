from agno.agent import Agent
from agno.models.groq import Groq
from agno.embedder.openai import OpenAIEmbedder  # Uncommented for embedding
import os
from dotenv import load_dotenv
from agno.knowledge.json import JSONKnowledgeBase
from agno.vectordb.pgvector import PgVector
from agno.tools.crawl4ai import Crawl4aiTools

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Configure embedder
embedder = OpenAIEmbedder()

knowledge_base = JSONKnowledgeBase(
    path="blacklisted.json",
    vector_db=PgVector(
        table_name="json_documents",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    ),
    embedder=embedder  # Include embedder
)

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    knowledge=knowledge_base,
    search_knowledge=True,
)

# Force recreation of embeddings
agent.knowledge.load(recreate=True)

# Test with a more specific query, explicitly asking for a list of names
agent.print_response("What are the names of 5 NGOs blacklisted by Uttar Pradesh?")

# You can also try this variation:
# agent.print_response("Give me a list of 5 blacklisted NGOs by Uttar Pradesh.")

# If the above still doesn't directly give you the list, it might be due to how the
# 'agno' library handles the response after searching the knowledge base.
# In some cases, the library might require a more conversational approach or a
# specific prompt format to extract and list the information.

# Here's another approach you could try, which is more direct in asking for the names:
# agent.print_response("List 5 'Name of NPODARPAN' that were 'Blacklisted By' 'Uttar Pradesh'.")

# If these direct prompts don't work, you might need to consult the 'agno' library's
# documentation for specific instructions on querying and extracting information
# from a JSONKnowledgeBase. Look for examples on how to format the output or if
# there are other methods in the 'Agent' class to achieve this.