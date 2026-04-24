from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# -------------------------------
# Load embedding model
# -------------------------------
# Using a lightweight SentenceTransformer model to generate embeddings
# for both bot personas and incoming posts (free + local, no API required)

model = SentenceTransformer("all-MiniLM-L6-v2")



# -------------------------------
# Embedding Wrapper
# -------------------------------
# LangChain expects an embedding interface with specific methods.
# This wrapper adapts SentenceTransformer to that interface.

class EmbeddingWrapper:
    def embed_documents(self, texts):
        return model.encode(texts).tolist()

    def embed_query(self, text):
        return model.encode([text])[0].tolist()

    def __call__(self, text):
        return self.embed_query(text)

embedding = EmbeddingWrapper()

# -------------------------------
# Bot Personas
# -------------------------------
# Each bot represents a different ideological viewpoint
# These will be embedded and stored in the vector database

bots = [
    ("bot_a", "I believe AI and crypto wil solve al human problems. I am highly optimistic about technology, Elon Musk, and space exploration. I dismiss regulatory concerns."),
    ("bot_b", "I believe late-stage capitalism and tech monopolies are destroying society. I am highly critical of AI, social media, and bi lionaires. I value privacy and nature."),
    ("bot_c", "I strictly care about markets, interest rates, trading algorithms, and making money. I speak in finance jargon and view everything through the lens of ROI.")
]

# -------------------------------
# Convert Personas into Documents
# -------------------------------
# Each persona is stored with metadata (bot_id)
# This allows retrieval of which bot matched after similarity search

docs = [
    Document(page_content=text, metadata={"bot_id": bot_id})
    for bot_id, text in bots
]

# -------------------------------
# Create Vector Database (FAISS)
# -------------------------------
# FAISS stores embeddings and enables fast similarity search
# We index all bot personas here

vector_db = FAISS.from_documents(docs, embedding)

# -------------------------------
# Routing Function
# -------------------------------

def route_post_to_bots(post_content: str, threshold: float = 1.2):

    """
    Routes an incoming post to relevant bots using vector similarity.

    Args:
        post_content (str): Incoming post text
        threshold (float): Distance threshold (lower = more similar)

    Returns:
        List of matched bots with similarity scores
    """

    # Perform similarity search (returns (Document, score))
    # NOTE: FAISS returns distance scores (not cosine similarity)
    # Lower score = higher similarity

    results = vector_db.similarity_search_with_score(post_content, k=3)

    matched = []

    for doc, score in results:
        if score <= threshold:  # lower = better
            matched.append({
                "bot_id": doc.metadata["bot_id"],
                "score": round(score, 3)
            })

    return matched

if __name__ == "__main__":
    print(route_post_to_bots("OpenAI just released a new model that might replace junior developers."))