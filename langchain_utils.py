import os
from dotenv import load_dotenv
import library as lib
from langchain_community.chat_message_histories import ChatMessageHistory
import db2
#import streamlit as st


load_dotenv()


def create_history(messages):
    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history

#@st.cache_resource
def invoke_chain(question):

    llm= lib.get_granite_code_model()
    nl2_sql_prompt = lib.get_nl2_sql_prompt(question)
    response = llm.invoke(nl2_sql_prompt)
    return response

#@st.cache_resource
def fix_query(response):
    query = lib.parse_response_to_sql(response)
    return query

#@st.cache_resource
def fix_query_by_llm(question, response):
    llm = lib.get_granite_code_model()
    corrected_query_prompt = lib.get_sql_correction_prompt(nl_query=question, sql_query=response)
    corrected_query = llm.invoke(corrected_query_prompt)
    return corrected_query

#@st.cache_resource
def get_db_result(corrected_query):
    result_df = db2.execute_query_df(corrected_query)
    return result_df


