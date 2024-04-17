import tempfile
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import os

google_api_key = os.getenv("GOOGLE_API_KEY")

def process_text(text, google_api_key):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_text(text)

    if not chunks:
        return None
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

def summarizer(pdf):
    if pdf is not None:
        try:
            loader = PyPDFLoader(pdf)
            pages = loader.load()

            text = "".join([page.page_content for page in pages if page.page_content])

            if text:
                knowledge_base = process_text(text, google_api_key)
                llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)  
                query = "Summarize the uploaded document in a 5 to 6 bullet points."

                if knowledge_base:
                    docs = knowledge_base.similarity_search(query)
                    if not docs:
                        return "No documents were found similar to the query."
                    else:
                        chain = load_qa_chain(llm, "stuff")
                        output = chain.run(input_documents=docs, question=query)
                        return output
        except Exception as e:
            return f"An error occurred: {e}"
    else:

        return "PDF file not found."
    
def save_uploadedfile(uploadedfile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploadedfile.getvalue())
        return tmp.name
