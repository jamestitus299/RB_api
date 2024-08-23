#  API -- FastAPI
A set of APIs for user registration, login, creating task and note lined to a user, implementing joins and chain delete functionality using FastApi and MongoDB

## Endpoints
    /user/register     -- Signup API: Endpoint to signup a new user. 
    /user/login        -- Login API: Endpoint to authenticate an existing user.
    /task/create       -- create a task and link to the user who created it 
    /task/user         -- retrives all tasks created by the user
    /note/create       -- create a note and link to the user who created it
    /note/user         -- retrives all notes created by the user

    - Joins: Implement functionality to join data from multiple collections.
    - Chain Delete: Implement functionality to delete a user and all associated data across collections.

# Getting started
Create a virtual environment and install the dependencies from the requirements.txt , then start the uvicorn server

or run

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload