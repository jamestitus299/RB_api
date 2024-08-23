
import os
from flask import Flask, jsonify
from fastapi import FastAPI, Form, HTTPException, Request, status

from models.user import User, UserResponse

# Flask app
# app = Flask(__name__)
app = FastAPI()


@app.get('/hello')
async def hello():
    return {'message': 'Hello from RB_API!'}, 200


@app.post('/register', response_model=UserResponse)
async def register(user:User):
    try:
        print(user)
        # ... your database interaction code ...

        return UserResponse.from_orm(user), status.HTTP_201_CREATED
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    



if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))   
    
