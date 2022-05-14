from utils import *
import streamlit as st



st.title('SHS Digitization Project')
st.markdown("### Convert '.doc' Files to CSV")
files = st.file_uploader("Upload Your File(s)", type=['.doc'], accept_multiple_files=True)
if files:
    df = combine_files(files)
    st.markdown("### Sample Data")
    st.write(df.head())
    new_file = df.to_csv().encode('utf-8')
    st.download_button('Download CSV', new_file, file_name='SHS.csv')

st.markdown("### Contact""")
st.markdown("For any issues or questions regarding using this application, contact Caleb Reigada at reigadacaleb@gmail.com")
