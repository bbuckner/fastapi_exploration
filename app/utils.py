from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(incoming_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(incoming_password, hashed_password)
