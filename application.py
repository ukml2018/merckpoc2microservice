from langchain_utils import invoke_chain, fix_query, fix_query_by_llm, get_db_result
from library import get_granite_model, get_granite_code_model, connect_to_database, get_nl2_sql_prompt, get_sql_correction_prompt, parse_response_to_sql
import json
from flask import Flask, jsonify
from flask_cors import CORS
import urllib
import sys
app = Flask(__name__)
CORS(app)
@app.route('/invokesearch/<user_query>', methods=['GET'])    
def invoke_search(user_query):
    
    if user_query:
        print(f"user_query={user_query}\n")
  
        try:
            response = invoke_chain(user_query)
            _FIXED_QUERY = fix_query(response)
            db_result = get_db_result(_FIXED_QUERY)

            if db_result.empty:
                _RESULT_KEY = False    
                _output = {
                "SQL": _FIXED_QUERY,
                "TABLEDATA": "No matching data found....",
                "KEY": _RESULT_KEY
                }
            else:
                _RESULT_KEY = True
                table_json = db_result.to_json(orient='records', date_format='iso')
                _output = {
                    "SQL": _FIXED_QUERY,
                    "TABLEDATA": table_json,
                    "KEY": _RESULT_KEY
                    }
            print(json.dumps(_output))
            return jsonify(_output)
    
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))
            #Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(error.read().decode("utf8", 'ignore')) 
                
            _RESULT_KEY = False  
            _output = {
                "SQL": "I'm afraid I am unable to generate an answer at this moment due to an error.",
                "TABLEDATA": '',
                "KEY": _RESULT_KEY
                }
            return jsonify(_output)
    
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            _RESULT_KEY = False  
            _output = {
                "SQL": "I'm afraid I am unable to generate an answer at this moment due to an error.",
                "TABLEDATA": '',
                "KEY": _RESULT_KEY
                }
            return jsonify(_output)
  
    else:
        print("Please provide a valid user query: can't proceed further")
        _RESULT_KEY = False 
        _output = {
            "SQL": "Please provide a valid user query: can't proceed further",
            "TABLEDATA": '',
            "KEY": _RESULT_KEY
            }
        return jsonify(_output)

if __name__ == '__main__':
    app.run(debug=True,port=5555)
