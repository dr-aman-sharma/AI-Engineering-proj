# Overview

A functional **Retrieval-Augmented Generation (RAG)** question-answering bot that allows users to upload PDF documents and ask natural language questions about their content. The bot intelligently searches through the document and provides accurate, context-aware answers using state-of-the-art AI models.


## Features

Behind the scenes, the bot performs intelligent semantic search using vector embeddings to find the most relevant information within the document. This ensures that answers are not just generic responses but are specifically tailored to the content of the uploaded PDF. The answers are generated using IBM watsonx.ai's Granite language model, which delivers high-quality, coherent, and context-aware responses. The web interface is built with Gradio, providing a clean, modern, and user-friendly experience across both desktop and mobile devices. 


### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | Gradio 5.0+ | Web interface & UI |
| **LLM** | IBM watsonx.ai (Granite-8b-Code-Instruct)| Answer generation |
| **Embeddings** | Hugging Face (all-MiniLM-L6-v2) | Text vectorization |
| **Vector DB** | ChromaDB | Semantic search & retrieval |
| **Document Processing** | PyPDFLoader + RecursiveCharacterSplitter | PDF parsing & chunking |
| **Language** | Python 3.11 | Core programming |

## How It Works

1. **Document Upload**: User uploads a PDF file
2. **Text Extraction**: Bot extracts text and splits into manageable chunks (500 chars with 50 overlap)
3. **Embedding Creation**: Converts text chunks into vector embeddings using sentence-transformers
4. **Vector Storage**: Stores embeddings in ChromaDB for fast similarity search
5. **Query Processing**: User's question is embedded and compared against stored vectors
6. **Context Retrieval**: Top 3 most relevant chunks are retrieved
7. **Answer Generation**: IBM Granite LLM generates a response based on retrieved context

## Prerequisites

- Python 3.11 or higher
- IBM Cloud account (for watsonx.ai API)

