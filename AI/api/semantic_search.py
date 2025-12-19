from langchain_community.document_loaders  import PyPDFLoader


file_path = "data/nke-10k-2023.pdf"

class SemanticSearch:
    def __init__(self):
        self.loader = PyPDFLoader(file_path)
        self.docs = self.loader.load()
        
    

