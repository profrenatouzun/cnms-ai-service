import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import MarkdownHeaderTextSplitter
from openaihelper import OpenAiHelper

CLOUD_DOCS_DB_DIRECTORY = 'db/cloud/'
UZUN_DOCS_DB_DIRECTORY = 'db/uzun/'

_ = load_dotenv(find_dotenv()) # read local .env file

helper = OpenAiHelper(os.environ["OPENAI_API_KEY"],os.environ["OPENAI_API_ENDPOINT"],os.environ["OPENAI_API_VERSION"])

# Load PDFs
cloudPdfloaders = [
    PyPDFLoader("material-de-apoio/COMPUTACAO_EM_NUVEM.pdf"),
    PyPDFLoader("material-de-apoio/51106265.pdf"),
    PyPDFLoader("material-de-apoio/2017_tcc_wfsilva.pdf"),
]
cloudDocs = []
for loader in cloudPdfloaders:
    cloudDocs.extend(loader.load())

# Split
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 150
)
cloudDocChunks = text_splitter.split_documents(cloudDocs)

vectordb = Chroma.from_documents(
    documents=cloudDocChunks,
    embedding=helper.getLangChainEmbeddings(),
    persist_directory=CLOUD_DOCS_DB_DIRECTORY
)

print(f"{CLOUD_DOCS_DB_DIRECTORY} created succefuly")

uzunData = open("renato.gobet.uzun.md", "r").read()

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

uzunDocChunks = markdown_splitter.split_text(uzunData)

uzunVectordb = Chroma.from_documents(
    documents=uzunDocChunks,
    embedding=helper.getLangChainEmbeddings(),
    persist_directory=UZUN_DOCS_DB_DIRECTORY
)

print(f"{UZUN_DOCS_DB_DIRECTORY} created succefuly")
