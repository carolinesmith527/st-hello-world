
import os
import pandas as pd
import csv
import json
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import gzip
import os
# import torch
import os, urllib
# , cv2
import streamlit as st

# This is the main app app itself, which appears when the user selects "Run the app".
def run_the_app():
    # To make Streamlit fast, st.cache allows us to reuse computation across runs.
    # In this common pattern, we download data from an endpoint only once.
    
    # st.write('Importing Data...')
    try:
        
        # load the dataset(knowledge base)
        embeddingsdf = pd.read_csv("./data/formatted_corpus.csv")
        st.write('## This is our Corpus:', embeddingsdf[:1000])

    except urllib.URLError as e:
            st.error(
                """
                **This demo requires internet access.**
                Connection error: %s
            """
                % e.reason
            )
# @st.cache()
st.markdown(
"""You can input a query or a question. The script then uses semantic search to find relevant passages in Simple English Wikipedia (as it is smaller and fits better in RAM).

For semantic search, we use SentenceTransformer('multi-qa-MiniLM-L6-cos-v1') and retrieve 32 potentially passages that answer the input query.

Next, we use a more powerful CrossEncoder (cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')) that scores the query and all retrieved passages for their relevancy. The cross-encoder further boost the performance, especially when you search over a corpus for which the bi-encoder was not trained for."""
)

# Once we have the dependencies, add a selector for the app mode on the sidebar.
st.sidebar.title("What to do")
app_mode = st.sidebar.selectbox("Choose the app mode",
    ["Show instructions", "Run the app"])
if app_mode == "Show instructions":
    st.sidebar.success('To continue select "Run the app".')
# elif app_mode == "Show the source code":
#     readme_text.empty()
#     st.code(get_file_content_as_string("streamlit_app.py"))
elif app_mode == "Run the app":
    # readme_text.empty()
    run_the_app()
      
# if __name__ == "__main__":
#     main()
