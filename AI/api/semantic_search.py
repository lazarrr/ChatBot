from langchain_community.document_loaders  import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from openai import embeddings


file_path = "data/nke-10k-2023.pdf"

class SemanticSearch:
    def __init__(self):
        self.loader = PyPDFLoader(file_path)
        self.docs = self.loader.load()
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    def get_all_chunks(self):
        chunks = self.text_splitter.split_documents(self.docs)
        return chunks
    
    def get_embeddings(self):
        chunks = self.get_all_chunks()
        vector_1 = embeddings.embed_query(chunks[0].page_content)
        vector_2 = embeddings.embed_query(chunks[1].page_content)

        assert len(vector_1) == len(vector_2)
        print(f"Generated vectors of length {len(vector_1)}\n")
        print(vector_1[:10])
        
    

