\---

title: RAG Question-Answering Bot

emoji: 🤖

colorFrom: blue

colorTo: green

sdk: gradio

sdk\_version: 5.0.0

app\_file: app.py

pinned: false

\---



\# RAG Question-Answering Bot



A Retrieval-Augmented Generation (RAG) bot that answers questions based on uploaded PDF documents.



\## Features



\- Upload any PDF document

\- Ask natural language questions

\- Get AI-powered answers based on document content

\- Powered by IBM watsonx.ai and Hugging Face embeddings



\## How it works



1\. Upload a PDF file

2\. The bot splits the text into chunks and creates embeddings

3\. When you ask a question, it retrieves relevant chunks

4\. An LLM generates an answer based on the retrieved context

