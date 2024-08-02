from typing import Optional, Tuple
import pandas as pd
from dotenv import load_dotenv
import os
#os.add_dll_directory('C:\\ProgramData\\clidriver\\bin')
os.environ["LD_LIBRARY_PATH"] = "/usr/local/lib/python3.11/site-packages/clidriver/bin"
#os.add_dll_directory("C:\\Users\\640240744\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python312\\site-packages\\clidriver\\bin")
import ibm_db
try:
    import ibm_db_dbi as db2  # pip install ibm_db
except ModuleNotFoundError as e:
    print(e)



def read_pandas_dataframe(db_metadata: dict, query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Read the table from db2 to a pandas DataFrame
    to run locally set DYLD_LIBRARY_PATH in environment variables (clidriver)
    export DYLD_LIBRARY_PATH=<clidriver_PATH>/lib:$DYLD_LIBRARY_PATH
    Args:
        db_metadata: db2 metadata dictionary
        query: SQL Query

    Returns:
        Tuple: pandas DataFrame
    """
    error = None
    df_res = None
    db2_dsn = "DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={uid};PWD={pwd};SECURITY=SSL".format(
        db_metadata["database"],
        db_metadata["host"],
        db_metadata.get("port", 32304),
        uid=db_metadata["username"],
        pwd=db_metadata["password"],
    )

    db2_connection = db2.connect(db2_dsn)
    try:
        df_res = pd.read_sql_query(query, con=db2_connection)
    except pd.errors.DatabaseError as e:
        error = f"error db2 {e}"
    return df_res, error


def get_db2_schema(db_metadata: dict):
    query = """SELECT schemaname FROM syscat.schemata;"""
    return read_pandas_dataframe(db_metadata=db_metadata, query=query)


def get_db2_tables(db_metadata: dict, table_schema: str):
    query = f"SELECT TABNAME,REMARKS  FROM syscat.tables WHERE TABSCHEMA = '{table_schema}';"
    return read_pandas_dataframe(db_metadata=db_metadata, query=query)


def get_db2_table_metadata(db_metadata: dict, table_name: str, table_schema: str):
    # KEYSEQ indicates a primary key
    query = (
        f"SELECT COLNAME,KEYSEQ,REMARKS  FROM syscat.columns WHERE TABNAME  = '{table_name}' "
        f"and TABSCHEMA = '{table_schema}';"
    )
    print(query)
    df = read_pandas_dataframe(db_metadata=db_metadata, query=query)
    print(df)
    return df


def get_db2_table_schema(db_metadata: dict, table_name: str, table_schema: str):
    query = (
        f"SELECT COLNAME,TYPENAME,REMARKS  FROM syscat.columns WHERE TABNAME  = '{table_name}'"
        f" and TABSCHEMA = '{table_schema}';"
    )
    return read_pandas_dataframe(db_metadata=db_metadata, query=query)


def execute_query_df(query: str):
    """Read the table from db2 to a pandas DataFrame
    to run locally set DYLD_LIBRARY_PATH in environment variables (clidriver)
    export DYLD_LIBRARY_PATH=<clidriver_PATH>/lib:$DYLD_LIBRARY_PATH
    Args:
        db_metadata: db2 metadata dictionary
        query: SQL Query

    Returns:
        Tuple: pandas DataFrame
    """
    error = None
    df_res = None
    server = "db2w-mgyhbny.us-south.db2w.cloud.ibm.com"
    port = 50001
    database = "BLUDB"
    username = "bluadmin"
    password = "gKpg5CIqlWWM1U@Oc_3x__7Cuqkh7"

    db2_dsn = "DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={uid};PWD={pwd};SECURITY=SSL".format(
    database,
    server,
    port,
    uid=username,
    pwd=password,
)

    db2_connection = db2.connect(db2_dsn)
    try:
        df_res = pd.read_sql_query(query, con=db2_connection)
    except pd.errors.DatabaseError as e:
        error = f"error db2 {e}"
    return df_res
