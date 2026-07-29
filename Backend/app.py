from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your new routers
from routes.chat_router import router as chat_router
from routes.upload_router import router as upload_router

# Initialize FastAPI
app = FastAPI(title="Offline SQL Agent API")

# Setup CORS (Crucial for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the routers to the main app
# We use prefix="/api" here so we don't have to write it in every single file
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(upload_router, prefix="/api", tags=["Upload"])