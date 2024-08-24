#  API -- FastAPI
A set of APIs for user registration, login, creating task and note lined to a user, implementing joins and chain delete functionality using FastApi and MongoDB

## Endpoints
    /user/signup       -- Endpoint to signup a new user. 
    /user/login        -- Endpoint to authenticate an existing user.
    /user/signup/admin -- Endpoint to signup an admin user

    /task/create       -- create a task and link to the user who created it 
    /task/user         -- retrives all tasks created by the user
    /task/all          -- retrieves all available tasks along with the user who created the task(join)
        (only for use by an admin user) 

    /note/create       -- create a note and link to the user who created it
    /note/user         -- retrives all notes created by the user
    /note/all          -- retrieves all notes along with the user who created the task(join)
        (only for use by an admin user) 

    /query/delete/user -- endpoint that chain deletes user, and the tasks and notes created by the user

# Getting started
    Create a virtual environment and install the dependencies from the requirements.txt , then start the uvicorn server

    or run:
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt

    start the server:
        uvicorn main:app --reload