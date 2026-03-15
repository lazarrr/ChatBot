from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from vectoreStore import VectoreStore
from langchain_classic.chains.summarize import load_summarize_chain
import os
import re

class Agent:
    def __init__(self):
        self.vectoreStore = VectoreStore()
        
        # FIXED: Use a valid OpenAI model
        self.llm = ChatOpenAI(
            model="gpt-5-mini",  # or "gpt-3.5-turbo" or "gpt-4"
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0
        )
        
        self.retriever = self.vectoreStore.getVectoreStore().as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 5}
        )

        # 1. Contextualize question sub-chain
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        self.history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, contextualize_q_prompt
        )

        # 2. Main QA chain
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, just say that you don't know. "
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        self.rag_chain = create_retrieval_chain(self.history_aware_retriever, question_answer_chain)

    def get_session_history(self, session_id: str):
        return SQLChatMessageHistory(
            session_id=session_id, 
            connection="sqlite:///chat_history.db"
        )

    def add_file_to_store(self, file_path: str):
        """Add a file to the vector store"""
        self.vectoreStore.store_file(file_path)

    def debug_retrieval(self, query: str):
        """Debug method to check what's being retrieved"""
        # Get documents directly from retriever
        docs = self.retriever.invoke(query)
        print(f"\n=== DEBUG: Retrieved {len(docs)} documents for query: '{query}' ===")
        
        if not docs:
            print("⚠️ No documents retrieved!")
            print("Check if:")
            print("1. Vector store has documents (run vectoreStore.getVectoreStore()._collection.count())")
            print("2. Document chunks were properly embedded")
            print("3. The query is relevant to your documents")
        else:
            for i, doc in enumerate(docs):
                print(f"\n--- Document {i+1} (score: {doc.metadata.get('score', 'N/A')}) ---")
                print(f"Source: {doc.metadata.get('source', 'Unknown')}")
                print(f"Preview: {doc.page_content[:200]}...")
        
        return docs

    def chat(self, message: str) -> str:
        # Handle summarize command
        summary_match = re.search(r"summarize\s+(?:of\s+|the\s+)?([\w\.-]+)", message.lower())
        if summary_match:
            filename = summary_match.group(1)
            return self.summarize_file(filename)

        # DEBUG: Check retrieval first (remove this in production)
        retrieved_docs = self.debug_retrieval(message)
        
        if not retrieved_docs:
            return "I couldn't find any relevant documents in my knowledge base. Please make sure you've added documents first."

        conversational_rag_chain = RunnableWithMessageHistory(
            self.rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        response = conversational_rag_chain.invoke(
            {"input": message},
            config={"configurable": {"session_id": "default_session"}}
        )
        
        return response["answer"]