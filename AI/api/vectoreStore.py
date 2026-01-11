from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders  import PyPDFLoader , TextLoader, Docx2txtLoader


class VectoreStore:
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
        
    def getVectoreStore(self):
        return self.vector_store
    
    def store_file(self, file_path):
        try:
            print("Loading documents...")
            if file_path.__contains__("pdf"):
                self.loader = PyPDFLoader(file_path)
            elif file_path.__contains__("docx"):
                self.loader = Docx2txtLoader(file_path)
            elif file_path.__contains__("txt"):
                self.loader = TextLoader(file_path)
            else:
                raise ValueError("Unsupported file format. Please use PDF, DOCX, or TXT files.")
            documents = self.loader.load()
            for doc in documents:
                doc.metadata['source_file'] = file_path.split('/')[-1]
                
            texts = self.text_splitter.split_documents(documents)
            self.vector_store.add_documents(texts)
        except Exception as e:
            print(f"Error storing file {file_path}: {str(e)}")
    
    def get_all_documents_by_filename(self, filename: str):
        all_docs = []
        
        # Use public index_to_docstore_id to get all doc IDs
        all_doc_ids = list(self.vector_store.index_to_docstore_id.values())
        
        for doc_id in all_doc_ids:
            doc = self.vector_store.docstore.search(doc_id)
            if doc == "not found":  # Skip if ID not found (shouldn't happen)
                continue
            if doc.metadata.get('source_file') == filename:
                all_docs.append(doc)
    
        return all_docs

    def search(self, query: str, k: int = 5):
        return self.vector_store.similarity_search(query, k=k)