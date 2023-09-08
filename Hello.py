import streamlit as st
import helper
import pandas as pd
APP_NAME = "Smart Search!"

st.set_page_config(
    page_title=APP_NAME,
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.markdown("Made with love using [streamlit](https://streamlit.io/)")
# st.sidebar.image(
#     "images/contact.png"
# )

st.sidebar.title(APP_NAME)

st.header(APP_NAME)

form_expander = st.expander(label='Contact Form')
with form_expander:
    sample_queries = [
        "YMCA Garfield",
        "company at address"
    ]       
    show = st.checkbox("Show Sample Queries")
    with st.form('Contact Form'):
        # name = st.text_input('Name: ')
        numresponses = st.text_input('Number of responses:',value=10)
        if show:
            query = st.selectbox('Select Sample Query:', sample_queries, key=1)
        else:
            query = st.text_input('Ask Query:', 'Pay Online')
        submitted = st.form_submit_button('Submit')

if submitted:
    # show the result response
    st.subheader("Result")
    top_k=int(numresponses)
    responses = helper.get_query_responses(query, top_k)
    # st.json(responses)
    responsesdf=pd.DataFrame.from_dict(responses,orient='index')
    st.dataframe(responsesdf)
    # st.success(f"Hello {name},\n{responses[0]['Response']}\nThanks")
