from langgraph.graph import StateGraph, END
from LangGraph.state import SQLState
from nodes.check_execution_status import check_execution_status
from nodes.execute_sql import execute_sql_node
from nodes.extract_schema import extract_schema_node
from nodes.generate_sql import generate_sql_node
from nodes.summarizer import summarize_node 

graph = StateGraph(SQLState)

graph.add_node("extract_schema", extract_schema_node)
graph.add_node("generate_sql", generate_sql_node)
graph.add_node("execute_sql", execute_sql_node)
graph.add_node("summarize", summarize_node) 

graph.set_entry_point("extract_schema")
graph.add_edge("extract_schema", "generate_sql")
graph.add_edge("generate_sql", "execute_sql")

graph.add_conditional_edges(
    "execute_sql",
    check_execution_status,
    {
        "retry": "generate_sql",   
        "success": "summarize"            
    }
)
graph.add_edge("summarize", END)

app = graph.compile()
