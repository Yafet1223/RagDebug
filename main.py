from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacter TextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI

)
from langchain_community.vectorstores import FAISS

from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

from langchain.chains import RetrievalQA
GOOGLE_API_KEY = "YOUR_API_KEY"
loader=TextLoader("error.txt")
documents=loader.load()
splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=50
)
docs=splitter.split_documents(documents)
embeddings
