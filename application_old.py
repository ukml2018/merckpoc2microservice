import os
#from pprint import pprint
from genai.credentials import Credentials
from genai.client import Client
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, AsyncQdrantClient
#from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores.types import MetadataInfo, VectorStoreInfo
from genai import Client
from genai.credentials import Credentials
from genai.extensions.llama_index import IBMGenAILlamaIndex
from genai.schema import DecodingMethod, TextGenerationParameters
from genai import Client
from genai.credentials import Credentials
from genai.extensions.langchain import LangChainInterface
from genai.schema import DecodingMethod, TextGenerationParameters
from langchain_core.prompts import PromptTemplate
from flask import Flask, jsonify
import urllib
from flask_cors import CORS
#import ibm_db

app = Flask(__name__)
# API endpoint for invoking the query
CORS(app)
@app.route('/invokesearch/<user_query>', methods=['GET'])    
def invoke_search(user_query):
    #API key generated from home page https://bam.res.ibm.com/
    GENAI_KEY= 'pak-UYp8ihym7m7HISk2h1V8y-QvaZwGk6w7vlNMI9BLDZg'
    #API endpoin (By deafult)
    GENAI_API='https://bam-api.res.ibm.com'
    api_key = GENAI_KEY
    api_endpoint =GENAI_API
    print(api_key)
    print(api_endpoint)
    credentials = Credentials(api_key=GENAI_KEY, api_endpoint=GENAI_API)

    watsonx_client = Client(credentials=credentials)
    query_model = LangChainInterface(
        client=watsonx_client,
        model_id="ibm/granite-34b-code-instruct",
        parameters=TextGenerationParameters(
            decoding_method=DecodingMethod.GREEDY,
            max_new_tokens=100,
            min_new_tokens=10
        ),
    )

    prompt_content_new= """
    [INST]<<SYS>>
    You are an DB2 expert,  write a syntactically correct DB2 query to run, then look at the results of the query and return the answer to the input question.
    You can order the results to return the most informative data in the database.
    follow these instructions :


    - Pay attention to use only the column names that you can see in the schema description in Table Fields Metadata.
    - Pay attention to which column is in which table.
    - Always qualify table name with schema

    - for complex queries with subqueries describe each building block of SQL query in Explanation section of your answer.
    - SQL query should end with semicolon character
    -you will limit only to writing queries
    -In the response provide only query, don't provide the question asked and other details.
    -SQL query should end with semicolon character
    -the date format should be yyyy-mm-dd only
    -don't include time stamp in the query results

    Here below are 3 examples of DB2 Query :

    example 1:

    Question: what was the longest project duration a manager worked ever worked on?

    Tables:
    | schema   | TABNAME   | table description                                                                                                                                                 |
    |:---------|:----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | KPT73043 | EMP       | contains information about the employees such as employee number, name, job title, hire date, salary, commision, department number and whether they are a manager |
    | KPT73043 | PROJ      | contains information about projects such as the project id, employee number assigned, start dates and end dates                                                   |

    Table Fields Metadata:

    Table EMP:
    | schema   | COLNAME   | TYPENAME   | field description                                                                              |
    |:---------|:----------|:-----------|:-----------------------------------------------------------------------------------------------|
    | KPT73043 | EMPNO     | INTEGER    | The employee number                                                                            |
    | KPT73043 | ENAME     | VARCHAR    | The employee name                                                                              |
    | KPT73043 | JOB       | VARCHAR    | The job title of the employee, either ['ANALYST'; 'CLERK'; 'MANAGER'; 'PRESIDENT'; 'SALESMAN'] |
    | KPT73043 | MGR       | INTEGER    | The employee number of the employee's manager                                                  |
    | KPT73043 | HIREDATE  | TIMESTAMP  | The date when the employee was hired                                                           |
    | KPT73043 | SAL       | INTEGER    | The salary of the emplopyee                                                                    |
    | KPT73043 | COMM      | INTEGER    | The commision earned by the employee                                                           |
    | KPT73043 | DEPTNO    | INTEGER    | The department number to which the employee belongs to                                         |


    Table PROJ:
    | schema   | COLNAME   | TYPENAME   | field description                                           |
    |:---------|:----------|:-----------|:------------------------------------------------------------|
    | KPT73043 | PROJID    | INTEGER    | The project id                                              |
    | KPT73043 | EMPNO     | INTEGER    | The employee number of the employee assigned to the project |
    | KPT73043 | STARTDATE | TIMESTAMP  | The start date of the employee assigned to the project      |
    | KPT73043 | ENDDATE   | TIMESTAMP  | The end date of the employee assigned to the project        |

    SQLQuery:

    SELECT MAX(ENDDATE - STARTDATE) AS LongestProjectDuration
    FROM KPT73043.EMP E
    JOIN KPT73043.PROJ P ON E.EMPNO = P.EMPNO
    AND E.DEPTNO IN (SELECT DEPTNO FROM KPT73043.EMP WHERE JOB = 'MANAGER');

    example 2:

    Question: what is the total salary mass for each department for managers with more than 5 years of service

    Tables:
    | schema   | TABNAME   | table description                                                                                                                                                 |
    |:---------|:----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | KPT73043 | DEPT      | contains information about the department such as department number, department name and the location                                                             |
    | KPT73043 | EMP       | contains information about the employees such as employee number, name, job title, hire date, salary, commision, department number and whether they are a manager |


    Table Fields Metadata:

    Table DEPT:
    | schema   | COLNAME   | TYPENAME   | field description                                                             |
    |:---------|:----------|:-----------|:------------------------------------------------------------------------------|
    | KPT73043 | DEPTNO    | INTEGER    | The department number                                                         |
    | KPT73043 | DNAME     | VARCHAR    | The departmnet name, either ['ACCOUNTING'; 'OPERATIONS'; 'RESEARCH'; 'SALES'] |
    | KPT73043 | LOC       | VARCHAR    | The location/city of the department                                           |


    Table EMP:
    | schema   | COLNAME   | TYPENAME   | field description                                                                              |
    |:---------|:----------|:-----------|:-----------------------------------------------------------------------------------------------|
    | KPT73043 | EMPNO     | INTEGER    | The employee number                                                                            |
    | KPT73043 | ENAME     | VARCHAR    | The employee name                                                                              |
    | KPT73043 | JOB       | VARCHAR    | The job title of the employee, either ['ANALYST'; 'CLERK'; 'MANAGER'; 'PRESIDENT'; 'SALESMAN'] |
    | KPT73043 | MGR       | INTEGER    | The employee number of the employee's manager                                                  |
    | KPT73043 | HIREDATE  | TIMESTAMP  | The date when the employee was hired                                                           |
    | KPT73043 | SAL       | INTEGER    | The salary of the emplopyee                                                                    |
    | KPT73043 | COMM      | INTEGER    | The commision earned by the employee                                                           |
    | KPT73043 | DEPTNO    | INTEGER    | The department number to which the employee belongs to                                         |


    SQLQuery:

    SELECT DEPT.DNAME, SUM(EMP.SAL) AS TotalSalary
    FROM KPT73043.DEPT DEPT
    JOIN KPT73043.EMP EMP ON DEPT.DEPTNO = EMP.DEPTNO
    WHERE EMP.JOB = 'MANAGER' AND EMP.HIREDATE < (CURRENT TIMESTAMP - INTERVAL '5 year')
    GROUP BY DEPT.DNAME;


    example 3:

    Question: what is number of junior (less 5 years),senior (5 to 10 years) and principal (more than 10 years) employees based their hiring date.

    Tables:
    | schema   | TABNAME   | table description                                                                                                                                                 |
    |:---------|:----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | KPT73043 | EMP       | contains information about the employees such as employee number, name, job title, hire date, salary, commision, department number and whether they are a manager |


    Table Fields Metadata:

    Table EMP:
    | schema   | COLNAME   | TYPENAME   | field description                                                                              |
    |:---------|:----------|:-----------|:-----------------------------------------------------------------------------------------------|
    | KPT73043 | EMPNO     | INTEGER    | The employee number                                                                            |
    | KPT73043 | ENAME     | VARCHAR    | The employee name                                                                              |
    | KPT73043 | JOB       | VARCHAR    | The job title of the employee, either ['ANALYST'; 'CLERK'; 'MANAGER'; 'PRESIDENT'; 'SALESMAN'] |
    | KPT73043 | MGR       | INTEGER    | The employee number of the employee's manager                                                  |
    | KPT73043 | HIREDATE  | TIMESTAMP  | The date when the employee was hired                                                           |
    | KPT73043 | SAL       | INTEGER    | The salary of the emplopyee                                                                    |
    | KPT73043 | COMM      | INTEGER    | The commision earned by the employee                                                           |
    | KPT73043 | DEPTNO    | INTEGER    | The department number to which the employee belongs to                                         |

    SQLQuery:

    WITH SENIORITY AS(
    SELECT EMP.EMPNO,
    CASE WHEN YEAR(CURRENT TIMESTAMP - EMP.HIREDATE)<=5 THEN 1 ELSE 0 END AS junior,
    CASE WHEN YEAR(CURRENT TIMESTAMP - EMP.HIREDATE)>5 AND YEAR(CURRENT TIMESTAMP - EMP.HIREDATE)<=10 THEN 1 ELSE 0 END AS senior,
    CASE WHEN YEAR(CURRENT TIMESTAMP - EMP.HIREDATE)>10 THEN 1 ELSE 0 END AS principal
    FROM EMP)
    SELECT SUM(JUNIOR) AS junior,SUM(SENIOR) AS senior,SUM(PRINCIPAL) AS principal FROM SENIORITY;


    <</SYS>>
    {query_str}
    {tables}
    {fields_meta}
    response should be only DB2 query which can be directly executed on the DB2 server, don't provide the question and any other information in the response.
    the date format should be yyyy-mm-dd only
    don't include time stamp in the query results
    DB2 query should always end with semicolon(;)
    [/INST]
    """

    tables = """
    | schema   | TABNAME   | table description                                                                                                                                                 |
    |:---------|:----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    |TSC_SA_T2 |MAT_DTL_GDSL_V| managing and tracking materials used in the manufacture of Gardasil. By providing detailed information on each material and component, including unique identifiers, part numbers, product families, and descriptions, this table supports efficient inventory management and production planning. It ensures that all necessary materials are available and properly documented for the production of Gardasil, contributing to the overall efficiency and quality of the manufacturing process.                                                            |
    """

    fields_meta ="""Table MAT_DTL_GDSL_V:
    | schema   | COLNAME   | TYPENAME    |
    |:---------|:----------|:-----------|
    | TSC_SA_T2 | CID_KEY    | VARCHAR    |
    | TSC_SA_T2 | COMPONENT_DTL     | VARCHAR    | 
    | TSC_SA_T2 | PART_NUMBER       | INTEGER    |
    | TSC_SA_T2 | PRODUCT_FAMILY      | VARCHAR    |   
    | TSC_SA_T2 | MATERIAL  | VARCHAR  |
    | TSC_SA_T2 | MATERIAL_DTL       | VARCHAR     | 
    """
    #query_str ="What are the materials used in Gardasil Manufacturer?"
    query_str =user_query

    output_correction_prompt = PromptTemplate(template=prompt_content_new, input_variables=["query_str","tables","fields_meta"],)
    final_correction_promt = output_correction_prompt.format(query_str=query_str, tables=tables,fields_meta=fields_meta)

    response = query_model.invoke(final_correction_promt)
    print(response)

    start = response.find('SE')
    end = response.find('<')
    query1= response[start:end]
    print(query1)
    os.environ["LD_LIBRARY_PATH"] = "/usr/local/lib/python3.11/site-packages/clidriver/bin"
    #import os
    #os.add_dll_directory("C:\\Users\\640240744\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python312\\site-packages\\clidriver\\bin")
    #os.add_dll_directory("C:\\Users\\002L6A744\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\clidriver\\bin")
    #os.add_dll_directory("/usr/local/lib/python3.11/site-packages/clidriver/bin")
    import ibm_db

    # Database credentials
    dsn_hostname =  'db2w-mgyhbny.us-south.db2w.cloud.ibm.com'
    dsn_port =  50001
    dsn_database = 'BLUDB'
    dsn_uid = 'bluadmin'
    dsn_pwd = 'gKpg5CIqlWWM1U@Oc_3x__7Cuqkh7'

    # Construct the connection string
    dsn = (
        "DRIVER={{IBM DB2 ODBC DRIVER}};"
        "DATABASE={0};"
        "HOSTNAME={1};"
        "PORT={2};"
        "PROTOCOL=TCPIP;"
        "UID={3};"
        "PWD={4};"
        "SECURITY=SSL;"
    ).format(dsn_database, dsn_hostname, dsn_port, dsn_uid, dsn_pwd)
    #print("Before Connection")
    conn = ibm_db.connect(dsn, "", "")
    #print(conn)

    import pandas as pd
    stmt = ibm_db.exec_immediate(conn, query1)
    rows = ibm_db.fetch_assoc(stmt)
    data = []
    try:
      # Fetch all rows from the result set
        while rows:
            data.append(rows.copy())
            rows = ibm_db.fetch_assoc(stmt)

        # Create a DataFrame from the list of rows
        df = pd.DataFrame(data)

        # Print the DataFrame to verify
        print(df)
        json_data = df.to_json(orient='records')
        return json_data
    except urllib.error.HTTPError as error:
      print("The request failed with status code: " + str(error.code))
    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
      print(error.info())
      print(error.read().decode("utf8", 'ignore'))
      return jsonify({'error': 'Failed to get Summary information from Azure ML endpoint'}), 500
    
if __name__ == '__main__':
    app.run(debug=True,port=5555)


