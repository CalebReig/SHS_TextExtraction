from extraction import extract_text
import streamlit as st



st.title('Hello')
file = st.file_uploader("Upload Your Text File")
if file:
    with open('uploaded_file.doc', 'wb') as f:
        f.write(file.read())
    df = extract_text('uploaded_file.doc')
    st.write(df.head())
