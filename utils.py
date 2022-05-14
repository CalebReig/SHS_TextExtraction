import streamlit as st
import pandas as pd
from extraction import extract_text

@st.cache
def combine_files(files):
    df = None
    for file in files:
        with open('uploaded_file.doc', 'wb') as f:
            f.write(file.read())
        if not df:
            df = extract_text('uploaded_file.doc')
        else:
            df = pd.concat(df, extract_text('uploaded_file.doc'), axis=0)
    st.markdown("### Sample Data")
    st.write(df.head())
    new_file = df.to_csv().encode('utf-8')
    st.download_button('Download CSV', new_file, file_name='SHS.csv')
