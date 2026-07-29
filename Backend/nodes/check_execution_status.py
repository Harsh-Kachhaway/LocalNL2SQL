from LangGraph.state import SQLState

def check_execution_status(state: SQLState):
    """
    If there is an error and retries are under 3, route back to SQL generation.
    Otherwise, complete the execution loop.
    """
    if state.get("error") and state.get("retry_count", 0) < 3:
        return "retry"
    return "success"

