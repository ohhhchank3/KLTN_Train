import os

import streamlit as st
from langchain.document_loaders import UnstructuredPDFLoader

import app1 as filepdf
import pdf_document as words
#
os.environ["GOOGLE_API_KEY"] = "AIzaSyBq-FAdWKYvDaA8IlVO8rOlIsySjxTYXs0"

st.set_page_config(page_title="ChatPDF", page_icon="📄")
st.header('Chat with your documents')
st.write('Has access to custom documents and can respond to user queries by referring to the content within those documents')
st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/shashankdeshpande/langchain-chatbot/blob/master/pages/4_%F0%9F%93%84_chat_with_your_documents.py)')

class CustomDataChatbot:

    def save_file(self, file):
        folder = 'tmp'
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_path = f'./{folder}/{file.name}'
        with open(file_path, 'wb') as f:
            f.write(file.getvalue())
        return file_path

    def setup_qa_chain(self, uploaded_files, file_types):
        # Load documents
        qa_chains = []
        for file, file_type in zip(uploaded_files, file_types):
            file_path = self.save_file(file)
            file_name_without_extension = os.path.splitext(file.name)[0]  # Loại bỏ phần mở rộng
            final_file_name = f"db_{file_name_without_extension}_{file_type}"
            if file_type == "PDF":
                qa_chain = filepdf.load_file(file_path,final_file_name)
            elif file_type == "Word":
                qa_chain = words.load_file(file_path)
            elif file_type == "Text":
                # Xử lý tệp văn bản đơn giản ở đây
                pass
            else:
                st.warning(f"Unsupported file format: {file_type}")
                continue
            
            qa_chains.append(qa_chain)

        return qa_chains

    def main(self):

        # User Inputs
        uploaded_files = st.sidebar.file_uploader(label='Upload files', type=['pdf','docx','txt'], accept_multiple_files=True)
        if not uploaded_files:
            st.error("Please upload supported documents to continue!")
            st.stop()

        file_types = st.sidebar.selectbox('Select processing mode for each file:', ['PDF', 'Word'], index=0, key='file_types')

        user_query = st.text_input(label="Ask me anything!")

        if uploaded_files and user_query:
            qa_chains = self.setup_qa_chain(uploaded_files, [file_types]*len(uploaded_files))

            st.write(f'User: {user_query}')

            with st.spinner("Processing..."):
                for i, qa_chain in enumerate(qa_chains):
                    response = ""
                    if file_types == "PDF":
                        response = filepdf.ask(user_query, qa_chain)
                    elif file_types == "Word":
                        response = words.ask(user_query, qa_chain)
                    st.text(f"Bot ({file_types}): {response}")

if __name__ == "__main__":
    obj = CustomDataChatbot()
    obj.main()
