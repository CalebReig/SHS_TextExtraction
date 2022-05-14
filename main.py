from extraction import extract_text
import streamlit as st
import pandas as pd



st.title('SHS Digitization Project')
st.markdown("### Convert '.doc' Files to CSV")
files = st.file_uploader("Upload Your File(s)", type=['.doc'], accept_multiple_files=True)
if files:
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
    st.download_button('Download CSV', buf, file_name='graph.png')

st.markdown("### Contact""")
st.markdown("For any issues or questions regarding using this application, contact Caleb Reigada at reigadacaleb@gmail.com")
