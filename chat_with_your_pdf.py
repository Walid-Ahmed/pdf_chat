# -*- coding: utf-8 -*-
"""Chat_with_Your_Pdf.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eYj6fNU7FC8bkKkIOui0PcseY5MzS5gb

## Install Required Packages
"""

!pip install wget #python package to download files from internet
#langchain a software development framework designed to simplify the creation of applications using large language models
!pip install langchain
!pip install faiss-cpu
#tiktoken is a fast BPE tokeniser for use with OpenAI's models
!pip install tiktoken 
#PyPDF2 is a free and open-source pure-python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files
!pip install PyPDF2
#we will use wget to download our pdf file
!pip install wget
# to work with openAI
!pip install openai

"""## Import packages"""

import wget
from langchain.embeddings.openai import OpenAIEmbeddings
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
import wget

"""## set your OpenAI key"""

#set your Open-AI key
#key="you_openAI_kEY"
import os
os.environ["OPENAI_API_KEY"] = key



"""## Download your pdf file"""

url="https://arxiv.org/pdf/2010.11929"
fileName=wget.download(url)

"""## Read, split and econde text from pdf"""

# read data from the file and put them into a variable called pdf_text
reader = PdfReader(fileName)
pdf_text = ''
for page in (reader.pages):
    text = page.extract_text()
    if text:
        pdf_text += text

pdf_text

# Define our text splitter
text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 1000, #thousand charctere
    chunk_overlap  = 200,
    length_function = len,
)

#Apply splitting
text_chunks = text_splitter.split_text(pdf_text)

len(text_chunks)

text_chunks[20]

# Use embeddings from OpenAI
embeddings = OpenAIEmbeddings()

#Convert text to embeddings
pdf_embeddings = FAISS.from_texts(text_chunks, embeddings)

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

chain = load_qa_chain(OpenAI(), chain_type="stuff")

"""## Start chatting with the pdf"""

query = "what is the title of the article?"
docs = pdf_embeddings.similarity_search(query)
print(len(docs))
chain.run(input_documents=docs, question=query)

query = "who are the authors of the article?"
docs = pdf_embeddings.similarity_search(query)
chain.run(input_documents=docs, question=query)

query = "How was the model accuracy?"
docs = pdf_embeddings.similarity_search(query)
chain.run(input_documents=docs, question=query)

query = "what was the the training dataset?"
docs = pdf_embeddings.similarity_search(query)
chain.run(input_documents=docs, question=query)

query = "How is this model different from other models?"
docs = pdf_embeddings.similarity_search(query)
chain.run(input_documents=docs, question=query)

query = "What is the conclousion of the paper?"
docs = pdf_embeddings.similarity_search(query)
chain.run(input_documents=docs, question=query)

query = "How old is the first author?"
docs = pdf_embeddings.similarity_search(query)
chain.run(input_documents=docs, question=query)

"""## Credit: 

ChatGPT for YOUR OWN PDF files with LangChain 
https://www.youtube.com/watch?v=TLf90ipMzfE&t=726s
"""