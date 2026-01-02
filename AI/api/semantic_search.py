from langchain_community.document_loaders  import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore


file_path = "data/nke-10k-2023.pdf"

class SemanticSearch:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = InMemoryVectorStore(self.embeddings)

    def get_all_chunks(self):
        chunks = self.text_splitter.split_documents(self.docs)
        return chunks
    
    def load_documents(self, path: str):
        try:
            print("Loading documents...")
            self.loader = PyPDFLoader(path)
            self.docs = self.loader.load()
        except Exception as e:
            raise Exception(f"Error loading documents: {str(e)}")
        
    def store_embeddings(self):
        try:
            print("Storing embeddings in vector store...")
            chunks = self.get_all_chunks()
            self.vector_store.add_documents(documents=chunks)
        except Exception as e:
            print(f"Error storing embeddings: {str(e)}")
        
    def run(self, path:str):
        self.load_documents(path)
        self.store_embeddings()
        
    def search_store(self, query: str, k: int = 5):
        try:
            print("Searching vector store...")
            results = self.vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Error searching vector store: {str(e)}")
        