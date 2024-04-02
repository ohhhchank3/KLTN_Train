import os

from langchain.chains import RetrievalQA
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import (ChatGoogleGenerativeAI,
                                    GoogleGenerativeAIEmbeddings)
from unstructured.cleaners.core import clean_extra_whitespace

os.environ["GOOGLE_API_KEY"] = "AIzaSyBq-FAdWKYvDaA8IlVO8rOlIsySjxTYXs0"

def load_file(file_path,name):
    loader = UnstructuredPDFLoader(file_path, post_processors=[clean_extra_whitespace])
    pages1 = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    texts = text_splitter.split_documents(pages1)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    persist_directory = f'{name}'
    vectordb = Chroma.from_documents(documents=texts,
                                      embedding=embeddings,
                                      persist_directory=persist_directory)
    retriever = vectordb.as_retriever(search_kwargs={"k": 20})
    llm = ChatGoogleGenerativeAI(model='gemini-pro',
                                 max_output_tokens=1024,
                                 temperature=0.0,
                                 top_p=0.0,
                                 top_k=40,
                                 convert_system_message_to_human=True)

    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type="stuff",
                                           retriever=retriever,
                                           return_source_documents=True)
    return qa_chain

def ask(question, qa_chain):
    llm_response = qa_chain(question)
    answer = llm_response["result"]
    return answer

def main():
    file_path = r"D:\5_3\demo\demo1.pdf"
    qa_chain = load_file(file_path)
    
    question = "Tên của giảng viên hướng dẫn"
    response = ask(question, qa_chain)
    print(response)

if __name__ == "__main__":
    main()
