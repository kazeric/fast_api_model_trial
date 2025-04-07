import sys
import json
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from handler import handler

app = FastAPI()

@app.post("/")
async def handle_request(request: Request):
    data = await request.json()
    result = handler(data)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)