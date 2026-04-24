from langgraph.graph import StateGraph
from typing import TypedDict
from langchain_groq import ChatGroq
import json

from dotenv import load_dotenv
load_dotenv()

# -------------------------------
# LLM Initialization
# -------------------------------
# Using Groq-hosted LLaMA model (free tier)
llm = ChatGroq(model="llama-3.1-8b-instant")

# -------------------------------
# Graph State Definition
# -------------------------------
# Shared state passed between nodes in LangGraph
# Each node reads/writes parts of this dictionary
class GraphState(TypedDict):
    bot_id: str
    persona: str
    topic: str
    search_results: str
    post_content: dict


# -------------------------------
# Mock Search Tool
# -------------------------------
# Simulates external retrieval (like SearxNG API)
# Returns hardcoded "real-world" context based on query
def mock_searxng_search(query: str):
    query = query.lower()

    if "crypto" in query:
        return "Bitcoin hits new all-time high after ETF approval"
    elif "ai" in query:
        return "AI models replacing junior developers"
    else:
        return "Global markets show mixed signals"


# -------------------------------
# Node 1: Decide Topic
# -------------------------------
# Uses LLM to choose a topic aligned with persona
def decide_topic(state):
    prompt = f"""
    You are this persona:
    {state['persona']}

    Decide ONE topic to post about today.
    Return ONLY the topic (no extra text).
    """
    topic = llm.invoke(prompt).content.strip()
    return {"topic": topic}

# -------------------------------
# Node 2: Search
# -------------------------------
# Retrieves context using mock search tool
def search(state):
    result = mock_searxng_search(state["topic"])
    return {"search_results": result}



# -------------------------------
# Node 3: Generate Post
# -------------------------------
# Uses persona + topic + retrieved context
# Produces structured JSON output

def generate_post(state):
    prompt = f"""
    Persona: {state['persona']}
    Topic: {state['topic']}
    Context: {state['search_results']}

    Generate a strong, opinionated tweet (max 280 chars).

    Return ONLY valid JSON:
    {{
        "bot_id": "{state['bot_id']}",
        "topic": "{state['topic']}",
        "post_content": "..."
    }}
    """

    raw_output = llm.invoke(prompt).content.strip()

    # remove markdown if present
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(raw_output)

        # CRITICAL FIX: if model nested JSON again
        if isinstance(parsed.get("post_content"), str) and parsed["post_content"].startswith("{"):
            inner = json.loads(parsed["post_content"])
            parsed = inner

    except:
        parsed = {
            "bot_id": state["bot_id"],
            "topic": state["topic"],
            "post_content": raw_output[:200]
        }

    return {"post_content": parsed}


# -------------------------------
# Build LangGraph Pipeline
# -------------------------------

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("decide", decide_topic)
    graph.add_node("search", search)
    graph.add_node("generate", generate_post)

    graph.set_entry_point("decide")
    graph.add_edge("decide", "search")
    graph.add_edge("search", "generate")

    return graph.compile()

# -------------------------------
# Test Execution
# -------------------------------

if __name__ == "__main__":
    graph = build_graph()

    result = graph.invoke({
        "bot_id": "bot_a",
        "persona": "Tech maximalist who loves AI and crypto"
    })

    print(result["post_content"])