from hashlib import sha256
from src.services.hasher_port import HasherPort
from os import urandom, getenv


class Hasher(HasherPort):
    def __init__(self):
        self.pepper = getenv("PEPPER", "lol") # TODO: Переделать на получение из Settings()
    
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
