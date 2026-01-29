from datetime import datetime, timedelta, timezone
import jwt

from src.schemas.user import UserSchemaBase
from src.schemas.token import JWTToken
from src.services.jwt.port import JWTServicePort


class JWTService(JWTServicePort):
    def __init__(self, alg: str, secret_key: str, exp_minutes: str):
        self.alg = alg
        self.secret_key = secret_key
        self.exp_minutes = exp_minutes

    def encode(self, user: UserSchemaBase) -> JWTToken:
        to_encode = {"id": str(user.id)}
        
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.alg)
        return JWTToken(access_token=encoded_jwt)

    def decode(self, token: JWTToken) -> UserSchemaBase:
        payload = jwt.decode(token.access_token, self.secret_key, algorithms=[self.alg])
        user = UserSchemaBase.model_validate(payload)
        return user
