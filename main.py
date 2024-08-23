
import os
from flask import Flask, jsonify
from fastapi import FastAPI, status


# Flask app
# app = Flask(__name__)
app = FastAPI()


@app.get('/hello')
async def hello():
    return {'message': 'Hello from RB_API!'}, 200





   

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))
    
