from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json
import asyncio
import os
from dotenv import load_dotenv

# Import the LangGraph app and your Pydantic schema
from LangGraph.graph import app as langgraph_app
from routes.schemas import QuestionRequest

load_dotenv()

# Initialize the router instead of a full FastAPI app
router = APIRouter()

async def langgraph_streamer(question: str):
    db_path = os.getenv("DB_PATH", "sample_company.db")
    
    initial_state = {
        "question": question,
        "db_path": db_path,
        "schema": "",
        "generated_sql": "",
        "sql_result": "",
        "error": ""
    }

    async for step_output in langgraph_app.astream(initial_state):
        json_data = json.dumps(step_output)
        yield f"data: {json_data}\n\n"
        await asyncio.sleep(0.1)

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    return StreamingResponse(
        langgraph_streamer(request.question), 
        media_type="text/event-stream"
    )