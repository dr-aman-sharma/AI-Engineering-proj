import sys
sys.stdout.reconfigure(line_buffering=True)

print("init", flush=True)

from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from ibm_watsonx_ai import Credentials
from langchain_ibm import WatsonxLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
import gradio as gr
import warnings
from langchain.prompts import PromptTemplate

warnings.filterwarnings('ignore')

print("1. Imports loaded successfully")

## LLM
def get_llm():
    print("2. Initializing LLM...")
    model_id = 'ibm/granite-8b-code-instruct'  # Using supported model
    
    parameters = {
        GenParams.MAX_NEW_TOKENS: 256,
        GenParams.TEMPERATURE: 0.5,
    }
    
    project_id = "skills-network"
    
    watsonx_llm = WatsonxLLM(
        model_id=model_id,
        url="https://us-south.ml.cloud.ibm.com",
        project_id=project_id,
        params=parameters,
    )
    
    print("3. LLM initialized successfully")
    return watsonx_llm

## Document loader
def document_loader(file):
    print(f"4. Loading document: {file}")
    loader = PyPDFLoader(file.name)
    loaded_document = loader.load()
    print(f"5. Document loaded, {len(loaded_document)} pages")
    return loaded_document

## Text splitter
def text_splitter(data):
    print("6. Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Smaller chunks for better processing
        chunk_overlap=50,
        length_function=len,
    )
    chunks = text_splitter.split_documents(data)
    print(f"7. Created {len(chunks)} chunks")
    
    # Print first few chunks for debugging
    for i, chunk in enumerate(chunks[:2]):
        print(f"   Chunk {i}: {chunk.page_content[:100]}...")
    
    return chunks

## Embedding model - Using Hugging Face (Most reliable)
def get_embeddings():
    print("8. Initializing Hugging Face embeddings...")
    
    # This uses a free, local embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("9. Hugging Face embeddings initialized successfully")
    return embeddings

## Vector db
def vector_database(chunks):
    print("10. Creating vector database...")
    embedding_model = get_embeddings()
    
    # Create vectordb with error handling
    try:
        vectordb = Chroma.from_documents(chunks, embedding_model)
        print("11. Vector database created successfully")
        return vectordb
    except Exception as e:
        print(f"Error creating vector database: {e}")
        raise e

## Retriever
def retriever(file):
    print("Starting retriever creation...")
    splits = document_loader(file)
    chunks = text_splitter(splits)
    
    if not chunks:
        raise ValueError("No text chunks were created from the PDF. The file might be empty or unreadable.")
    
    vectordb = vector_database(chunks)
    retriever_obj = vectordb.as_retriever(search_kwargs={"k": 3})  # Return top 3 chunks
    print("12. Retriever ready")
    return retriever_obj

## QA Chain
prompt_template = """Use the following context to answer the question. 
If you don't know, say "I don't know."

Context: {context}

Question: {question}

Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)
def retriever_qa(file, query):
    try:
        print(f"13. Processing query: {query[:50]}...")
        
        if not query or query.strip() == "":
            return "Please enter a question."
        
        llm = get_llm()
        retriever_obj = retriever(file)
        
        qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever_obj,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT})
        
        print("14. Executing QA chain...")
        response = qa.invoke(query)
        print("15. Response received")
        
        # Print the actual response content
        answer = response['result']
        print(f"ANSWER: {answer}")  # This will show in terminal
        
        # If answer is empty, return a message
        if not answer or answer.strip() == "":
            return "No answer found. Please try a different question."
        
        return answer
    
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)
        return error_msg
# Create Gradio interface
rag_application = gr.Interface(
    fn=retriever_qa,
    flagging_mode="never",
    inputs=[
        gr.File(label="Upload PDF File", file_count="single", file_types=['.pdf'], type="filepath"),
        gr.Textbox(label="Input Query", lines=2, placeholder="Type your question here...")
    ],
    outputs=gr.Textbox(label="Output Response"),
    title="RAG Question-Answering Bot",
    description="Upload a PDF document and ask any question. The bot will search the document for answers."
)

# Launch the app
rag_application.launch(share=True)