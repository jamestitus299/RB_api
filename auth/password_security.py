from passlib.context import CryptContext

# password encrypt and validata
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)