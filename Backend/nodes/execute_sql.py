import sqlite3
from LangGraph.state import SQLState

def execute_sql_node(state: SQLState):
    """
    Executes the generated SQL query against the SQLite database.
    If successful, returns the query results in 'final_result'.
    If an error occurs, stores the error message in 'error'.
    """
    db_path = state["db_path"]
    sql_query = state["generated_sql"]
       
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        
        conn.close()
        
        return {
            "final_result": {"columns": column_names, "rows": rows},
            "error": ""
        }
        
    except Exception as e:
        error_msg = f"SQL Execution Error: {str(e)}"
        print(f"{error_msg}")
        return {
            "final_result": [],
            "error": error_msg
        }