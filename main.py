
import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from fastapi import FastAPI

from api import task, note, auth

load_dotenv()

# App
# app = Flask(__name__)
app = FastAPI()


app.include_router(auth.router)
app.include_router(task.router, prefix="/task")
app.include_router(note.router, prefix="/note")


if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))   
    
