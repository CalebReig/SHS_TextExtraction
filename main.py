from utils import *
import streamlit as st



st.title('SHS Digitization Project')
st.markdown("### Convert '.doc' Files to CSV")
st.markdown("**WARNING**: It may take up to 5-10 minutes to process based on number of files uploaded")
files = st.file_uploader("Upload Your File(s)", type=['.doc'], accept_multiple_files=True)
if files:
    df = combine_files(files)
    st.markdown("### Sample Data")
    st.write(df.head())
    new_file = df.to_csv()
    st.download_button('Download CSV', new_file, file_name='SHS.csv', encoding='utf-8')

st.markdown("### Contact""")
st.markdown("For any issues or questions regarding using this application, contact Caleb Reigada at reigadacaleb@gmail.com")
