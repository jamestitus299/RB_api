import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Union, Any
# from jose import jwt

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]   # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]    # should be kept secret

print(JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY )