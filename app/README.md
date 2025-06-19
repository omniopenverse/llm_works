# RAG Pipeline for PDF Question Answering


## Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline to enable question answering over PDF documents. The pipeline extracts text from PDFs, processes it into manageable chunks, generates embeddings, stores them in a vector database, and uses a Large Language Model (LLM) to generate accurate, context-aware responses based on user queries.



## General Workflow

- PDF Text Extraction: Extract raw text from uploaded PDF documents.

- Text Splitting: Divide the extracted text into smaller chunks for efficient processing.

- Embedding Generation: Convert text chunks into numerical vectors capturing semantic meaning.

- Vector Store Creation: Index embeddings in a vector database for fast similarity search.

- LLM Integration: Use a local LLM to generate responses based on retrieved relevant chunks.


## Prerequisites

- Python 3.8+: Ensure Python is installed.

-  If you want to use local LLM inference via Ollama. Download and install Ollama from [https://ollama.com/download](https://ollama.com/download). Ensure the ollama CLI is available (`which ollama`). Ollama must be running to use local models like `llama3.1:latest`, `llama3.2:3b`. For this session, pull these simple models. Do this 

```
ollama run llama3.1
```
Then, do this 

```
ollama run llama3.2
```
Also pull embedding models

```
ollama pull nomic-embed-text
```

Hardware: At least 8GB RAM; GPU recommended for faster LLM inference.



## To run the App: Installation

- Clone the repository:
```
git clone <https://github.com/omniopenverse/lab_rag.git>
cd lab_rag
```
- Install dependencies from the provided requirements.txt:

```
pip install -r requirements.txt
```

- Ensure ollama server is running
```
ollama serve
```

- Run the Streamlit application:


```
streamlit run app.py
```


##  How it works

The application reads the PDF and splits the text into smaller chunks that can be then fed into a LLM. It uses Ollama embeddings to create vector representations of the chunks. The application then finds the chunks that are semantically similar to the question that the user asked and feeds those chunks to the LLM to generate a response. The application uses Streamlit to create the GUI and Langchain to deal with the LLM.


## Contributing

This repository is for educational purposes only. Feel free to customize it to your needs.


