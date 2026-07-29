from typing import TypedDict


class SQLState(TypedDict):
    db_path: str
    question: str
    schema: str
    generated_sql: str
    error: str
    final_result: dict
    final_answer: str 
    retry_count: int  