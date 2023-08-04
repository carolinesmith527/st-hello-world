# # DATE_COLUMN = 'date/time'
# # DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
# #          'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# # @st.cache_data

# # def load_data(nrows):
# #     data = pd.read_csv(DATA_URL, nrows=nrows)
# #     lowercase = lambda x: str(x).lower()
# #     data.rename(lowercase, axis='columns', inplace=True)
# #     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
# #     return data

# # # Create a text element and let the reader know the data is loading.
# # data_load_state = st.text('Loading data...')
# # # Load 10,000 rows of data into the dataframe.
# # data = load_data(10000)
# # # Notify the reader that the data was successfully loaded.
# # data_load_state.text("Done! (using st.cache_data)")

# # if st.checkbox('Show raw data'):
# #     st.subheader('Raw data')
# #     st.write(data)

# # st.subheader('Number of pickups by hour')
# # hist_values = np.histogram(
# #     data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# # st.bar_chart(hist_values)
# # hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
# # filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
# # st.subheader(f'Map of all pickups at {hour_to_filter}:00')
# # st.map(filtered_data)

# st.set_page_config(
#     page_title="Hello",
#     page_icon="👋",
# )

# st.write("# Welcome to Streamlit! 👋")

# st.sidebar.success("Select a demo above.")

# st.markdown(
#     """
#     Streamlit is an open-source app framework built specifically for
#     Machine Learning and Data Science projects.
#     **👈 Select a demo from the sidebar** to see some examples
#     of what Streamlit can do!
#     ### Want to learn more?
#     - Check out [streamlit.io](https://streamlit.io)
#     - Jump into our [documentation](https://docs.streamlit.io)
#     - Ask a question in our [community
#         forums](https://discuss.streamlit.io)
#     ### See more complex demos
#     - Use a neural net to [analyze the Udacity Self-driving Car Image
#         Dataset](https://github.com/streamlit/demo-self-driving)
#     - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
# """
# )
# 
import os
import pandas as pd
import csv
import json
# from sentence_transformers import SentenceTransformer, CrossEncoder, util
import gzip
import os
# import torch
import os, urllib
# , cv2
import streamlit as st
st.markdown(
"""You can input a query or a question. The script then uses semantic search to find relevant passages in Simple English Wikipedia (as it is smaller and fits better in RAM).

For semantic search, we use SentenceTransformer('multi-qa-MiniLM-L6-cos-v1') and retrieve 32 potentially passages that answer the input query.

Next, we use a more powerful CrossEncoder (cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')) that scores the query and all retrieved passages for their relevancy. The cross-encoder further boost the performance, especially when you search over a corpus for which the bi-encoder was not trained for."""
)
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
    # readme_text.empty()
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
