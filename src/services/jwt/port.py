from typing import Protocol
from src.schemas.user import UserSchemaBase
from src.schemas.token import JWTToken


class JWTServicePort(Protocol):
    alg: str
    secret_key: str
    exp_minutes: str

    def encode(self, user: UserSchemaBase) -> JWTToken: ...
    def decode(self, token: JWTToken) -> UserSchemaBase: ...
