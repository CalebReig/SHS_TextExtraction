import streamlit as st
import pandas as pd
from extraction import extract_text

@st.cache
def combine_files(files):
    df = None
    for file in files:
        with open('uploaded_file.doc', 'wb') as f:
            f.write(file.read())
        if df is None:
            df = extract_text('uploaded_file.doc')
        else:
            df = pd.concat(df, extract_text('uploaded_file.doc'), axis=0)
    return df

