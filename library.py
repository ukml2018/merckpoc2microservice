import sqlalchemy as sa
from genai import Client
from genai.credentials import Credentials
from genai.schema import DecodingMethod, TextGenerationParameters
from genai.extensions.langchain import LangChainInterface
import prompts
import os
#os.add_dll_directory('C:\\ProgramData\\clidriver\\bin')
#os.add_dll_directory("C:\\Users\\640240744\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python312\\site-packages\\clidriver\\bin")
os.environ["LD_LIBRARY_PATH"] = "/usr/local/lib/python3.11/site-packages/clidriver/bin"
import ibm_db


def get_granite_model():

    GENAI_KEY="pak-dVVlfY0Kvk9beKOowpTB1pqL5GQDOkq7E1kydwg3WNc"
    GENAI_API="https://bam-api.res.ibm.com"
    credentials = Credentials(api_key=GENAI_KEY, api_endpoint=GENAI_API)
    watsonx_client = Client(credentials=credentials)

    model_id="ibm/granite-13b-chat-v2"
    #model_id = "ibm/granite-13b-chat-v2",
    parameters=TextGenerationParameters(
        decoding_method=DecodingMethod.GREEDY,
        repetition_penalty=1.05,
        max_new_tokens=1024,
        min_new_tokens=1,
        
    )
    watsonx_llm_granite = LangChainInterface(
        client=watsonx_client,
        model_id=model_id,
        parameters=parameters,
    )

    return watsonx_llm_granite


def get_granite_code_model():

    GENAI_KEY="pak-dVVlfY0Kvk9beKOowpTB1pqL5GQDOkq7E1kydwg3WNc"
    GENAI_API="https://bam-api.res.ibm.com"
    credentials = Credentials(api_key=GENAI_KEY, api_endpoint=GENAI_API)
    watsonx_client = Client(credentials=credentials)

    model_id="ibm/granite-34b-code-instruct"
    #model_id = "ibm/granite-13b-chat-v2",
    parameters=TextGenerationParameters(
        decoding_method=DecodingMethod.GREEDY,
        repetition_penalty=1.05,
        max_new_tokens=1024,
        min_new_tokens=1,        
    )

    watsonx_llm_granite = LangChainInterface(
        client=watsonx_client,
        model_id=model_id,
        parameters=parameters,
    )

    return watsonx_llm_granite

def connect_to_database():
    server = "db2w-mgyhbny.us-south.db2w.cloud.ibm.com"
    port = 50001
    database = "BLUDB"
    username = "bluadmin"
    password = "gKpg5CIqlWWM1U@Oc_3x__7Cuqkh7"

    connection_string = sa.URL.create(f"db2+ibm_db://{username}:{password}@{server}:{port}/{database}?Security=SSL")
    db_engine = sa.create_engine(connection_string)
    
    db_connection = db_engine.connect()
    return db_connection


def get_nl2_sql_prompt(nl_query):

    base_prompt = prompts.generate_sql_prompt
    final_sql_generation_prompt= base_prompt.format(query=nl_query)
    return final_sql_generation_prompt


def get_sql_correction_prompt(nl_query, sql_query):

    correction_prompt = prompts.answer_prompt
    final_sql_correction_prompt= correction_prompt.format(question=nl_query, query=sql_query)
    return final_sql_correction_prompt



def parse_response_to_sql(response: str) -> str:
    """
    takes an llm generated string as input and returns a tuple of two strings
    1) SQL query that was extracted from the input string
    2) Explanation of how SQL query was constructed

    :param response: str: Parse the response from the user
    :return: A tuple of two strings
    """
    #start_delimiter = "SELECT"
    #end_delimilter = ";"
    print("Trying to fix query")
    start_delimiters = [":",] #alternative: tell it to start and end with triple ''' (see Sprint 2 Final Copy prompt_content function)
    end_delimilter = ";"
    for delimeter in start_delimiters:
        sql_query_start = response.find(delimeter)
        if sql_query_start != -1:
            print("Found Delimerer:" + delimeter)
            query = response[sql_query_start+1:]
            response = query
        sql_query_end = query.find(end_delimilter)
        if sql_query_end != -1:
            query = query[: sql_query_end + len(end_delimilter)]
            response = query

        response = response.replace("\\","")
        response = response.replace("```","")
        response = response.replace("sql","")

        return response.strip()
