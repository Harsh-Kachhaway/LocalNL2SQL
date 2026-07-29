import sqlite3
from LangGraph.state import SQLState

def extract_schema_node(state: SQLState):
    """
    Connects to the SQLite database, extracts the schema, 
    and updates the state so the LLM can use it.
    """
    db_path = state["db_path"]
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        schema = "\n".join([table[0] for table in tables if table[0] is not None])
        conn.close()
        return {"schema": schema, "error": ""}
        
    except Exception as e:
        return {"error": f"Failed to extract schema: {str(e)}"}

