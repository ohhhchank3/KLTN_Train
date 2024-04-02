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

global qa_chain 
def load_file(file_path):
    global qa_chain 
    loader = UnstructuredPDFLoader(file_path,post_processors=[clean_extra_whitespace],)
    pages1 = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    texts = text_splitter.split_documents(pages1)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    persist_directory = 'db_9'
    vectordb = Chroma.from_documents(documents=texts,
                                 embedding=embeddings,
                                 persist_directory=persist_directory)
    retriever = vectordb.as_retriever(search_kwargs={"k":20})
    llm = ChatGoogleGenerativeAI(model='gemini-pro',
                    max_output_tokens=1024,
                    temperature=0.0,
                    top_p=0.0,
                    top_k=40,convert_system_message_to_human=True)

    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                  chain_type="stuff",
                                  retriever=retriever,
                                  return_source_documents=True)
    query = "Trình quản lý hội thoại là gì"
    llm_response = qa_chain(query)
    answer = llm_response["result"]

    return answer
    


def ask(question):
    global qa_chain 
    llm_response = qa_chain(question)
    answer = llm_response["result"]

    return answer

as1 = load_file(r"D:\5_3\demo\demo1.pdf")
response = ask("tên giảng viên phản biện cung cấp trong đoạn văn bản")
print(response)
print(as1)






