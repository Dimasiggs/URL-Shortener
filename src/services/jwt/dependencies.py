from dotenv import load_dotenv
import os

from src.services.jwt.service import JWTService
from src.services.jwt.port import JWTServicePort

load_dotenv(override=True)

def get_jwt_service() -> JWTServicePort:
    secret_key = os.getenv("SECRET_KEY", "lol")
    alg = os.getenv("ALGORITHM", "HS256")
    exp_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    return JWTService(
        alg,
        secret_key,
        exp_minutes
    )
