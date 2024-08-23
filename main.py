
import os
from dotenv import load_dotenv
# from flask import Flask, jsonify
from fastapi import FastAPI
from fastapi.responses import FileResponse

from api import task, note, auth, status

load_dotenv()

# App
# app = Flask(__name__)
app = FastAPI()

@app.get("/", description="Serves the Html File", tags=["root"])
async def root():
    return FileResponse("src/index.html")

# routes for endpoints
app.include_router(auth.router, prefix="/user")
app.include_router(task.router, prefix="/task")
app.include_router(note.router, prefix="/note")
app.include_router(status.router)


if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))   
    
