from extraction import extract_text
import streamlit as st



st.title('SHS Digitization Project')
st.markdown("### Convert '.doc' Files to CSV")
files = st.file_uploader("Upload Your File(s)", type=['.doc'], accept_multiple_files=True)
if files:
    combine_files(files)

st.markdown("### Contact""")
st.markdown("For any issues or questions regarding using this application, contact Caleb Reigada at reigadacaleb@gmail.com")
