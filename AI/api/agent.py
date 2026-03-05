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
        self.llm = ChatOpenAI(
            model="gpt-5-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0
        )
        self.retriever = self.vectoreStore.getVectoreStore().as_retriever(search_type="similarity", search_kwargs={"k": 5})

        # 1. Define a sub-chain that "re-phrases" the question based on history
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history."
            "If user asked for some personal information, and if that information is present in the vector store, then include that information in the standalone question. " \
            "you must retrieve any relevant information from the vector store and include it in the standalone question. " 
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, contextualize_q_prompt
        )

        # 2. Define the main QA chain
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question."
            "If user asked for some personal information, and if that information is present in the vector store, then include that information in the standalone question. " \
            "you must retrieve any relevant information from the vector store and include it in the standalone question. " 
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        self.rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    def get_session_history(self, session_id: str):
        return SQLChatMessageHistory(
            session_id=session_id, 
            connection="sqlite:///chat_history.db"
        )

    def summarize_file(self, filename: str) -> str:
        
        docs_to_summarize = self.vectoreStore.get_all_documents_by_filename(filename)

        print(f"Found {len(docs_to_summarize)} documents for file '{filename}' to summarize.")

        if not docs_to_summarize:
            return f"I couldn't find any data for a file named '{filename}'. Please ensure it was uploaded correctly."

        summarize_chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        
        try:
            summary = summarize_chain.invoke(docs_to_summarize)
            return summary["output_text"]
        except Exception as e:
            print(f"Error during summarization: {str(e)}")
            return f"Error during summarization: {str(e)}"

    def chat(self, message: str) -> str:
       
        summary_match = re.search(r"summarize\s+(?:of\s+|the\s+)?([\w\.-]+)", message.lower())
        print(f"Summary match: {summary_match}")
        if summary_match:
            filename = summary_match.group(1)
            return self.summarize_file(filename)

        # Otherwise, proceed with normal RAG chat
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
    
    def add_file_to_store(self, file_path: str):
        self.vectoreStore.store_file(file_path)