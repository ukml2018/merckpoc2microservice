
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

def get_current_date(timestamp=None):
    date_obj = {}
    if timestamp:
        current_date = datetime.fromtimestamp(timestamp).date()
    else:
        current_date = datetime.now().date()
        
    date_obj['current_date'] = current_date

    if current_date.month in [1, 2, 3]:
        date_obj['current_quarter']=1    
        date_obj['last_quarter_number'] = 4
        date_obj['next_quarter_number']=2
        date_obj['current_quarter_first_day'] =  datetime(current_date.year, 1, 1).date()
        date_obj['current_quarter_last_day'] = datetime(current_date.year, 3, 31).date()
        date_obj['last_quarter_first_day'] = datetime(current_date.year - 1, 10, 1).date()
        date_obj['last_quarter_last_day'] =  datetime(current_date.year - 1, 12, 31).date()
        date_obj['next_quarter_first_day'] = datetime(current_date.year, 4, 1).date()
        date_obj['next_quarter_last_day'] =  datetime(current_date.year, 6, 30).date()
    elif current_date.month in [4, 5, 6]:
        date_obj['current_quarter']=2   
        date_obj['last_quarter_number'] = 1
        date_obj['next_quarter_number']=3
        date_obj['current_quarter_first_day'] =  datetime(current_date.year, 4, 1).date()
        date_obj['current_quarter_last_day'] = datetime(current_date.year, 6, 30).date()
        date_obj['last_quarter_first_day'] = datetime(current_date.year, 1, 1).date()
        date_obj['last_quarter_last_day'] =  datetime(current_date.year, 3, 31).date()
        date_obj['next_quarter_first_day'] = datetime(current_date.year, 7, 1).date()
        date_obj['next_quarter_last_day'] =  datetime(current_date.year, 9, 30).date()
    elif current_date.month in [7, 8, 9]:
        date_obj['current_quarter']=3    
        date_obj['last_quarter_number'] = 2
        date_obj['next_quarter_number']=4
        date_obj['current_quarter_first_day'] =  datetime(current_date.year, 7, 1).date()
        date_obj['current_quarter_last_day'] = datetime(current_date.year, 9, 30).date()
        date_obj['last_quarter_first_day'] = datetime(current_date.year, 4, 1).date()
        date_obj['last_quarter_last_day'] =  datetime(current_date.year, 6, 30).date()
        date_obj['next_quarter_first_day'] = datetime(current_date.year, 10, 1).date()
        date_obj['next_quarter_last_day'] =  datetime(current_date.year, 12, 31).date()
    else:
        date_obj['current_quarter']=4    
        date_obj['last_quarter_number'] = 3
        date_obj['next_quarter_number']=1
        date_obj['current_quarter_first_day'] =  datetime(current_date.year, 10, 1).date()
        date_obj['current_quarter_last_day'] = datetime(current_date.year, 12, 31).date()
        date_obj['last_quarter_first_day'] = datetime(current_date.year, 7, 1).date()
        date_obj['last_quarter_last_day'] =  datetime(current_date.year, 9, 30).date()
        date_obj['next_quarter_first_day'] = datetime(current_date.year + 1, 1, 1).date()
        date_obj['next_quarter_last_day'] =  datetime(current_date.year+1, 3, 31).date()

    date_obj['current_year_first_day'] = datetime(current_date.year, 1, 1).date()
    date_obj['current_year_last_day'] = datetime(current_date.year, 12, 31).date()
    date_obj['next_year_first_day'] = datetime(current_date.year+ 1, 1, 1).date()
    date_obj['next_year_last_day'] = datetime(current_date.year+1, 12, 31).date()
    
    this_month_start = current_date.replace(day=1)
    date_obj['current_month_first_day'] = this_month_start
    go_to_nxt_mth= this_month_start + timedelta(days=32)
    next_month_start = go_to_nxt_mth.replace(day=1)
    date_obj['current_month_last_day'] = next_month_start - timedelta(days=1)
    date_obj['next_month_first_day'] = next_month_start
    go_to_next_to_next_month = next_month_start.replace(day=28) + timedelta(days=4)
    date_obj['next_month_last_day'] = go_to_next_to_next_month - timedelta(days=go_to_next_to_next_month.day) 
    last_day_of_last_month = this_month_start - timedelta(days=1)
    date_obj['last_month_last_day'] =last_day_of_last_month
    date_obj['last_month_first_day'] =last_day_of_last_month.replace(day=1)
    date_obj['november_first_day'] = datetime(current_date.year, 11, 1).date()
    date_obj['november_last_day'] = datetime(current_date.year, 11, 30).date()

    date_obj['week_from_now'] = current_date + timedelta(days=7)
    date_obj['last_week_from_now'] = current_date - timedelta(days=7)
    date_obj['next_two_weeks_from_now'] = current_date + timedelta(days=14)
    
    return date_obj


date_obj = get_current_date()

generate_sql_prompt =ChatPromptTemplate.from_messages([
    ("system" ,"""You are an expert SQL query writer. Generate a syntactically accurate IBM DB2 query that addresses an input question based on the following context.
     Do not try to generate any SQL query if you are unable to find relevant information in the given context. Do not hallucinate.
    
Inventory:
    1. Zero Inventory = Out of Stock  
    2. Below Minimum = Stock level is below the lowest quantity of a product that a company wants to have on hand at any given time to avoid stockouts
    3. Below SS  = Below Safety Stock level
    4. Above SS  = Above Safety Stock level    
        
        
Context for Quarter, month, year, and timelines:
    Now or today is """ + f"'{date_obj['current_date']}' " + """.
    Current week (or this week, or within a week) is from """ + f"'{date_obj['current_date']}'" + """ to """ + f"'{date_obj['week_from_now']}'" + """, next two weeks (or within 2 weeks) is from """ + f"'{date_obj['current_date']}'" + """ to """ + f"'{date_obj['next_two_weeks_from_now']}'" + """, and so on.
    Last week is from """ + f"'{date_obj['last_week_from_now']}'" + """ to """ + f"'{date_obj['current_date']}'" + """. 
    There are four quarters in a year. First Quarter (Q1) is from January to March. Second quarter (Q2) is from April to June. Third Quarter (Q3) is from July to September. Fourth Quarter (Q4) is from October to December. 
    Today's date is """ + f"{date_obj['current_date']}, so current quarter is Q{date_obj['current_quarter']}," + f"so use date BETWEEN {date_obj['current_quarter_first_day']} AND {date_obj['current_quarter_last_day']}. Previous quarter is Q{date_obj['last_quarter_number']}, so use date BETWEEN {date_obj['last_quarter_first_day']} AND {date_obj['last_quarter_last_day']}. Next quarter is Q{date_obj['next_quarter_number']}, so use date BETWEEN {date_obj['next_quarter_first_day']} AND {date_obj['next_quarter_last_day']}. This year is from {date_obj['current_year_first_day']} to {date_obj['current_year_last_day']}. Next year is from {date_obj['next_year_first_day']} to {date_obj['next_year_last_day']}. Next month is from {date_obj['next_month_first_day']} to {date_obj['next_month_last_day']}. Previous month is from {date_obj['last_month_first_day']} to {date_obj['last_month_last_day']}. NQ or CQ+1 means Next Quarter. CQ+2 means next to the next quarter. Similarly, CM+1 means next month. CM+2 means next to next month, and so on. If the question contains the name of a month, consider it as the month of the current year. For example, November is from {date_obj['november_first_day']} to {date_obj['november_last_day']}." + """
    Quarter representations may take different formats such as yyQx, Qxyy, yyyyQx. 
    Examples - 22Q2 or 22q2 means Q2 of year 2022, 1Q16 or 1q16 means Q1 of year 2016, 2022Q3 or 2022q3 means Q3 of year 2022, fourth qtr means Q4 of the current year.


Please use the following abbreviations and terms consistently:                 
    CQ = Current quarter
    Last Quarter = Previous Quarter
    LQ = Last Quarter
    CY = Current Year
    NY = Next Year
    CM = Current Month
    CM +1 = Next Month
    QTR = Quarter
    qtr = quarter


Here are schema details:

Tables:
| schema    | TABNAME                    | table description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|:----------|:---------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TSC_SA_T2 | PO_DETAILS_V               | This table serves as a detailed repository for managing purchase orders scheduled for the next quarter. It includes critical information about order creation and delivery dates, lead times, supplier details, and order statuses. This table supports efficient planning and management of future purchase orders, ensuring that the supply chain operates smoothly and that materials are delivered on time to meet production requirements.                                                                                                |
| TSC_SA_T2 | MAT_DETAILS_V              | This table serves as a critical resource for managing and tracking materials used in the manufacture of Gardasil. By providing detailed information on each material and component, including unique identifiers, part numbers, product families, and descriptions, this table supports efficient inventory management and production planning. It ensures that all necessary materials are available and properly documented for the production of Gardasil, contributing to the overall efficiency and quality of the manufacturing process. |
| TSC_SA_T2 | ON_HAND_INV_V              | This table serves as a vital resource for managing the on-hand inventory of various components. By providing essential information on unique identifiers, material details, and the quantity of unrestricted stocks, this table supports efficient inventory management. It ensures that inventory levels are accurately tracked and that sufficient stocks are available to meet production and operational requirements.                                                                                                                     |
| TSC_SA_T2 | INV_PROJ_V                 | This table serves as a critical resource for forecasting inventory levels at the end of the third quarter. It provides essential data on material IDs, detailed descriptions, latest transaction dates, and projected inventory quantities. This table supports inventory planning and management by offering insights into future inventory needs, helping organizations prepare for upcoming demand and manage their supply chain effectively.                                                                                               |
| TSC_SA_T2 | DEMAND_VS_SUPPLY_WKS_MAT_V | This table serves as a critical resource for identifying demands and supply of materials on weekly basis. It provides essential data on material IDs, part_number, material and component descriptions, cumulative demand, cumulative suppy on weekly basis.                                                                                                                                                                                                                                                                                   |
| TSC_SA_T2 | INV_COV_MOC_V              | This table maintains inventory data that indicates the weekly and monhtly coverage of the demand                                                                                                                                                                                                                                                                                                                                                                                                                                               |

REMEMBER: ou must only use the tables listed above to generate SQL queries.

Table Fields Metadata:

Table PO_DETAILS_V:
| schema    | COLNAME        | TYPENAME   | field description                                                                                                                                                             |
|:----------|:---------------|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TSC_SA_T2 | CID_KEY        | VARCHAR    | Unique identifier which is a combination of the part number and the plant ID. It ensures the uniqueness of each material entry                                                |                                                                           |
| TSC_SA_T2 | MATERIAL       | VARCHAR    | This column stores the material ID, a unique identifier for each material used in manufacturing a part. It helps in tracking and managing inventory.                          |
| TSC_SA_T2 | PO_NUM         | VARCHAR    | This column holds the unique identifier for each purchase order. It is essential for order tracking and reference                                                             |
| TSC_SA_T2 | OPEN_QTY       | DECIMAL    | This column indicates the quantity of the order that is not yet fulfilled. It helps in identifying the outstanding amount of material that is still due for delivery          |
| TSC_SA_T2 | SUPPLIER_NAME  | VARCHAR    | This column stores the name of the supplier from whom the materials are being sourced. It helps in identifying and managing supplier relationships                            |        
| TSC_SA_T2 | CREATED_DATE   | DATE       | This column stores the date when the purchase order was created. It helps in tracking when the order was initiated                                                            |
| TSC_SA_T2 | DELIVERED_DATE | DATE       | This column records the date when the purchase order is expected to be delivered. It helps in managing delivery schedules and ensuring timely receipt of goods.               |
| TSC_SA_T2 | CONFIRMED      | VARCHAR    | This column indicates whether the purchase order has been confirmed by the supplier. It helps in managing order statuses and ensuring that orders are acknowledged            |
| TSC_SA_T2 | LEADTIME       | INTEGER    | This column indicates the lead time required to fulfill the purchase order. It is typically measured in days and helps in planning and scheduling.                            |
| TSC_SA_T2 | LINE_ITEM      | INTEGER    | This column represents the line item number within the purchase order. Each purchase order can have multiple line items, each corresponding to a specific material or product |

Table MAT_DETAILS_V:
| schema    | COLNAME        | TYPENAME   | field description                                                                                                                                                   |
|:----------|:---------------|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TSC_SA_T2 | CID_KEY        | VARCHAR    | Unique identifier which is a combination of the part number and the plant ID. It ensures the uniqueness of each material entry                                      |
| TSC_SA_T2 | MATERIAL       | VARCHAR    | This column stores the material ID, a unique identifier for each material used in manufacturing  a part. It helps in tracking and managing inventory.               |
| TSC_SA_T2 | MATERIAL_DTL   | VARCHAR    | This column provides a detailed description of the material. It includes comprehensive information about the material's characteristics and specifications.         |
| TSC_SA_T2 | PART_NUMBER    | VARCHAR    | This column stores the part number of the component or material. It uniquely identifies each part used in the manufacturing process.                                |
| TSC_SA_T2 | PRODUCT_FAMILY | VARCHAR    | This column indicates the manufacturer to which the material or component belongs. It helps in categorizing and managing materials based on their product family.   |
| TSC_SA_T2 | COMPONENT_DTL  | VARCHAR    | This column contains detailed information about the component used in the manufacturing process. It provides specific details necessary for the production          |

Table ON_HAND_INV_V:
| schema    | COLNAME             | TYPENAME   | field description                                                                                                                                                                                                                 |
|:----------|:--------------------|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TSC_SA_T2 | CID_KEY             | VARCHAR    | Unique identifier which is a combination of the part number and the plant ID. It ensures the uniqueness of each material entry                                                                                                    |
| TSC_SA_T2 | MATERIAL            | VARCHAR    | This column stores the material ID, a unique identifier for each material used in manufacturing  a part. It helps in tracking and managing inventory.                                                                             |
| TSC_SA_T2 | MATERIAL_DTL        | VARCHAR    | This column provides a detailed description of the material. It includes comprehensive information about the material's characteristics and specifications.                                                                       |
| TSC_SA_T2 | COMPONENT_DTL       | VARCHAR    | This column contains detailed information about the component used in the manufacturing process. It provides specific details necessary for the production                                                                        |
| TSC_SA_T2 | PRODUCT_FAMILY      | VARCHAR    | This column indicates the manufacturer to which the material or component belongs. It helps in categorizing and managing materials based on their product family.                                                                 |
| TSC_SA_T2 | UNRESTRICTED_STOCKS | INTEGER    | This column indicates the quantity of stocks that are not subject to any restrictions and are available for immediate use or sale. It helps in understanding the available inventory that can be utilized without any constraints.|
| TSC_SA_T2 | INVENTORY_LEVEL     | VARCHAR    | This column provides a detailed description of the material. It includes comprehensive information about the material's characteristics and specifications.                                                                       |

Table INV_PROJ_V:
| schema    | COLNAME                   | TYPENAME   | field description                                                                                                                                           |
|:----------|:--------------------------|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TSC_SA_T2 | CID_KEY                   | VARCHAR    | Unique identifier which is a combination of the part number and the plant ID. It ensures the uniqueness of each material entry                              |
| TSC_SA_T2 | PART_NUMBER               | VARCHAR    | Unique identifier of the part number                                                                                                                        |
| TSC_SA_T2 | COMPONENT_DTL             | VARCHAR    | This column contains detailed information about the component used in the manufacturing process. It provides specific details necessary for the production  |
| TSC_SA_T2 | INVENTORY_PROJECTION      | DECIMAL    | Projected inventory quantity of the material                                                                                                                |
| TSC_SA_T2 | INVENTORY_PROJECTION_DATE | DATE       | Date of Inventory Projection                                                                                                                                |


Table DEMAND_VS_SUPPLY_WKS_MAT_V:
| schema    | COLNAME       | TYPENAME   | field description                                                                                                                                           |
|:----------|:--------------|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TSC_SA_T2 | CID_KEY       | VARCHAR    | Unique identifier which is a combination of the part number and the plant ID. It ensures the uniqueness of each material entry                              |
| TSC_SA_T2 | MATERIAL      | VARCHAR    | This column stores the material ID, a unique identifier for each material used in manufacturing  a part. It helps in tracking and managing inventory.       |
| TSC_SA_T2 | MATERIAL_DTL  | VARCHAR    | This column provides a detailed description of the material. It includes comprehensive information about the material's characteristics and specifications. |
| TSC_SA_T2 | PART_NUMBER   | VARCHAR    | This column stores the part number of the component or material. It uniquely identifies each part used in the manufacturing process.                        |
| TSC_SA_T2 | DEMAND_WK     | BIGINT     | This column indicates the weekly demand of the material for the particular week.                                                                            |
| TSC_SA_T2 | SUPPLY_WK     | BIGINT     | This column indicates the weekly supply of the material for the particular week.                                                                            |
| TSC_SA_T2 | WK_FROM       | DATE       | Starting date of the week                                                                                                                                   |
| TSC_SA_T2 | WK_FROM       | DATE       | Starting date of the week                                                                                                                                   |
| TSC_SA_T2 | DEMAND_CUM    | DATE       | Cumulative demand                                                                                                                                           |
| TSC_SA_T2 | SUPPLY_CUM    | DATE       | Cumulative supply                                                                                                                                           |

Table INV_COV_MOC_V:
| schema    | COLNAME              | TYPENAME   | field description                                                                                                                                                   |
|:----------|:---------------------|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TSC_SA_T2 | CID_KEY              | VARCHAR    | Unique identifier which is a combination of the part number and the plant ID. It ensures the uniqueness of each material entry                                      |
| TSC_SA_T2 | CM_PLANT             | CHARACTER  | This column holds the unique identifier for the Contract Manufacturer plant. It is typically a short code representing the plant.                                   |
| TSC_SA_T2 | CM_NAME              | VARCHAR    | This column stores the name of the Contract Manufacturer (CM) plant. It identifies the specific plant responsible for manufacturing the ordered material.           |
| TSC_SA_T2 | MATERIAL             | VARCHAR    | This column stores the material ID, a unique identifier for each material used in manufacturing  a part. It helps in tracking and managing inventory.               |
| TSC_SA_T2 | PART_NUMBER          | VARCHAR    | This column stores the part number of the component or material. It uniquely identifies each part used in the manufacturing process.                                |
| TSC_SA_T2 | PRODUCT_FAMILY       | VARCHAR    | This column indicates the manufacturer to which the material or component belongs. It helps in categorizing and managing materials based on their product family.   |
| TSC_SA_T2 | COMPONENT_DTL        | VARCHAR    | This column contains detailed information about the component used in the manufacturing process. It provides specific details necessary for the production          |
| TSC_SA_T2 | INVENTORY_PROJECTION | DECIMAL    | Projected inventory quantity of the material                                                                                                                        |
| TSC_SA_T2 | MRP_PROJECTION       | DATE       | Inventory projection date                                                                                                                                           |
| TSC_SA_T2 | INV_COV_DAYS         | DECIMAL    | How many day the inventory will cover the demand                                                                                                                    |
| TSC_SA_T2 | INV_COV_MONTHS       | INTEGER    | How many months the inventory will cover the demand                                                                                                                 |

Here are seven examples of Question and corresponding SQLQuery:

"Question": "What is my days of coverage for the component XXX at Harlem?"
"SQLQuery": "SELECT * FROM TSC_SA_T2.INV_COV_MOC_V WHERE COMPONENT_DTL='XXX' and UPPER(CM_NAME) LIKE UPPER('Harlem%');"
Done:"Stop here"

"Question": "Which  components are used for material XXX?"
"SQLQuery": "select DISTINCT MAT_DETAILS.MATERIAL, MAT_DETAILS.MATERIAL_DTL, MAT_DETAILS.COMPONENT_DTL, MAT_DETAILS.CID_KEY FROM TSC_SA_T2.MAT_DETAILS_V MAT_DETAILS WHERE UPPER(MATERIAL_DTL) LIKE UPPER('XXX%');"
Done:"Stop here"

"Question": "Are there any open purchase orders?"
"SQLQuery": "SELECT * FROM TSC_SA_T2.PO_DETAILS_V;"
Done:"Stop here"

"Question": "What are my purchase orders for the LQ?"
"SQLQuery": "SELECT * FROM TSC_SA_T2.PO_DETAILS_V WHERE DELIVERED_DATE BETWEEN """ + f"'{date_obj['last_quarter_first_day']}' AND '{date_obj['last_quarter_last_day']}' " + """;" 
Done:"Stop here"

"Question": "How many purchase orders have been closed last month?"
"SQLQuery": "SELECT COUNT(*) FROM TSC_SA_T2.PO_DETAILS_V WHERE DELIVERED_DATE BETWEEN """ + f"'{date_obj['last_month_first_day']}' AND '{date_obj['last_month_last_day']}' " + """;"
Done:"Stop here"

"Question": "What was my demand for material XXXX right now?"
"SQLQuery": "SELECT DISTINCT DMND_SPPLY.CID_KEY, DMND_SPPLY.MATERIAL, DMND_SPPLY.MATERIAL_DTL, DMND_SPPLY.DEMAND_CUM from TSC_SA_T2.DEMAND_VS_SUPPLY_WKS_MAT_V DMND_SPPLY WHERE WK_TO BETWEEN """ + f"'{date_obj['current_date']}'" + """ AND """ + f"'{date_obj['week_from_now']}' " + """ AND UPPER(MATERIAL_DTL) LIKE UPPER('XXX%');"
Done:"Stop here"

"Question": "What is my supply for material XXXX right now?"
"SQLQuery": "SELECT DISTINCT DMND_SPPLY.CID_KEY, DMND_SPPLY.MATERIAL, DMND_SPPLY.MATERIAL_DTL, DMND_SPPLY.SUPPLY_CUM from TSC_SA_T2.DEMAND_VS_SUPPLY_WKS_MAT_V DMND_SPPLY WHERE WK_TO BETWEEN """ + f"'{date_obj['current_date']}'" + """ AND """ + f"'{date_obj['week_from_now']}' " + """ AND UPPER(MATERIAL_DTL) LIKE UPPER('XXX%');"
Done:"Stop here"

"Question": "Which Gardasil components currently have no stock available?"
"SQLQuery": "SELECT * FROM TSC_SA_T2.ON_HAND_INV_V WHERE UPPER(INVENTORY_LEVEL) like UPPER('%Zero Inventory') AND UPPER(PRODUCT_FAMILY) like UPPER('%GARDASIL%');"
Done:"Stop here"

"Question": "What are my hobbies?"
"SQLQuery": "Sorry, I am unable to generate SQL query for this question."
Done:"Stop here"
----------------------------------------------------------------- END OF EXAMPLES ---------------------------------------------------------------------------------------

Format the generated SQL output as follows.
Question:
SQLQuery:  
Done:"Stop here" 

    

Strictly follow the below rules while constructing the SQL Query:

- Always use UPPER function for columns in where clause to match the filter values. Also transform the filter values in the question to uppercase to match.
- Always use LIKE operator to match String columns in the filter.
- Always Use SELECT DISTINCT to avoid duplicates.
- Do not use entire table_name as table_alias.
- Ensure that the SQL query is concise and do not repeat the column names.
- To limit result set use 'LIMIT'. Never use the term "TOP" to limit result set.
- Do not add quotes for the column alias.
- If not asked in the question, do not limit the data.
- If there is a month or quarter filter, do include year and month filters.
- You can use IN or NOT IN Operators in the WHERE clause to specify multiple possible values.
- Pay attention to TIMESTAMP and DATE field types in filters. you can use BETWEEN DATE() to filter a TIMESTAMP.
- Use only relevant columns specified in Table Fields Metadata section given the input Question.
- Pay attention to use only the column names that you can see in the schema description in Table Fields Metadata.
- DO not query for columns that do not exist.
- Pay attention to which column is in which table.
- Always use qualify table name with schema.
- For complex queries with subqueries describe each building block of SQL query in Explanation section of your answer.
- SQL query should end with semicolon character.
- Only FILTER and SELECT on necessary fields given in the input Question.
      
      

Always remember that you must only use the tables listed above to generate SQL queries. 
If you are unable to find any table that is relevant to the question, do not try to generate SQL query. Just respond saying - 'Sorry, I am unable to generate SQL query.'

Now generate SQLQuery for the below question. Strictly follow the below format -

Question: {query}
SQLQuery:
Done:"Stop here"
"""),
("human","{query}")]
)


answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query generated by LLM, return only the query query from the response.

Question: {question}
SQLQuery: {query}
Answer: """
)

