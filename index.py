import streamlit as st
from utils import summarizer, save_uploadedfile

def main():
    
    st.set_page_config(page_title="PDF Summarizer", page_icon=":page:", layout="wide")

    st.title("PDF Summarizer")
    st.write("This is a simple web app to summarize the content of a PDF file.")
    st.divider()

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    submit = st.button("Summarize")

    if submit:
        if uploaded_file is None:
            st.warning("Please upload a PDF file.")
        else:           
            file_path = save_uploadedfile(uploaded_file)
            output = summarizer(file_path)
            st.subheader("Summary: ")
            st.write(output)

if __name__ == "__main__":
    main()