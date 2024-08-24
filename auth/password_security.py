from passlib.context import CryptContext

# password encrypt and validata
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt_password(password: str):
    """
        returns the encrypted password 
    """
    return pwd_context.encrypt(password)


def check_encrypted_password(password :str , hashed_password: str):
    """
        returns if the password and hashed_password are the same
    """
    return pwd_context.verify(password, hashed_password)