'''You can input a query or a question. The script then uses semantic search to find relevant passages in Simple English Wikipedia (as it is smaller and fits better in RAM).

For semantic search, we use SentenceTransformer('multi-qa-MiniLM-L6-cos-v1') and retrieve 32 potentially passages that answer the input query.

Next, we use a more powerful CrossEncoder (cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')) that scores the query and all retrieved passages for their relevancy. The cross-encoder further boost the performance, especially when you search over a corpus for which the bi-encoder was not trained for.'''

import os
import pandas as pd
import csv
import json
# from sentence_transformers import SentenceTransformer, CrossEncoder, util
import gzip
import os
import torch
import os, urllib, cv2
import streamlit as st

# inputf = "https://github.com/carolinesmith527/st-hello-world/blob/983fd62f96da1a1ea2de1df428d8ee9a164f08d1/formatted_corpus.csv"
# Streamlit encourages well-structured code, like starting execution in a main() function.
# def main():
# Render the readme as markdown using st.markdown.
# readme_text = st.markdown(get_file_content_as_string("instructions.md"))

# Download external dependencies.
# for filename in EXTERNAL_DEPENDENCIES.keys():
#     download_file(filename)

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
    readme_text.empty()
    run_the_app()
      
# This is the main app app itself, which appears when the user selects "Run the app".
def run_the_app():
    # To make Streamlit fast, st.cache allows us to reuse computation across runs.
    # In this common pattern, we download data from an endpoint only once.
    @st.cache()
    
    def load_metadata():
        inputf = "https://github.com/carolinesmith527/st-hello-world/blob/983fd62f96da1a1ea2de1df428d8ee9a164f08d1/formatted_corpus.csv"
        return pd.read_csv(inputf)
    
    # st.write('Importing Data...')
    try:
        embeddingsdf = load_metadata()
        st.write('## This is our Corpus:', embeddingsdf[:1000])
    except URLError as e:
            st.error(
                """
                **This demo requires internet access.**
                Connection error: %s
            """
                % e.reason
            )
            
# inputf = "https://github.com/carolinesmith527/st-hello-world/blob/983fd62f96da1a1ea2de1df428d8ee9a164f08d1/formatted_corpus.csv"
# if __name__ == "__main__":
#     main()
