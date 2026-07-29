import uvicorn

if __name__ == "__main__":
    # Running it this way strictly prevents any file-watching loops
    print("Starting server WITHOUT file-watching...")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)