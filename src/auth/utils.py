from hashlib import sha256
from os import urandom
from datetime import datetime, timedelta, timezone
import jwt
from sqlalchemy import UUID


from src.config import settings
from src.utils import singleton

from src.auth.interfaces import HasherPort
from src.auth.interfaces import JWTServicePort



@singleton
class Hasher(HasherPort):
    def __init__(self, pepper: str, salt_len: int = 5):
        self.salt_len = salt_len
        self.pepper = pepper

    def encode(self, text: str, salt: str) -> str:
        data = text + salt + self.pepper
        data = data.encode()
        hashed_data = sha256(data).hexdigest()

        return hashed_data

    def verify(self, text: str, salt: str, hashed_text: str) -> bool:
        return self.encode(text, salt) == hashed_text

    @property
    def salt(self) -> str:
        return urandom(self.salt_len).hex()



class JWTService(JWTServicePort):
    def __init__(self, alg: str, secret_key: str, exp_minutes: str):
        self.alg = alg
        self.secret_key = secret_key
        self.exp_minutes = exp_minutes

    def encode(self, user_id: UUID) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"id": str(user_id), "exp": expire}

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.alg)
        return encoded_jwt

    def decode(self, access_token: str) -> dict:
        payload = jwt.decode(access_token, self.secret_key, algorithms=[self.alg])
        
        return payload
