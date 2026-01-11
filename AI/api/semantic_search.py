from langchain_community.document_loaders  import PyPDFLoader , TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS


class SemanticSearch:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        embedding_dim = len(self.embeddings.embed_query("hello world"))
        index = faiss.IndexFlatL2(embedding_dim)
        self.vector_store = FAISS(
                                embedding_function=self.embeddings,
                                index=index,
                                docstore=InMemoryDocstore(),
                                index_to_docstore_id={},
                            )

    def get_all_chunks(self):
        chunks = self.text_splitter.split_documents(self.docs)
        return chunks
    
    def load_documents(self, path: str):
        try:
            print("Loading documents...")
            if path.__contains__("pdf"):
                self.loader = PyPDFLoader(path)
            elif path.__contains__("docx"):
                self.loader = Docx2txtLoader(path)
            elif path.__contains__("txt"):
                self.loader = TextLoader(path)
            else:
                raise ValueError("Unsupported file format. Please use PDF, DOCX, or TXT files.")
            self.docs = self.loader.load()
        except Exception as e:
            print(f"Error loading documents: {str(e)}")
        
    def store_embeddings(self):
        try:
            print("Storing embeddings in vector store...")
            chunks = self.get_all_chunks()
            print("Number of chunks to store:", len(chunks))
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
        