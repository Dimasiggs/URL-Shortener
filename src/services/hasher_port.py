from typing import Protocol


class HasherPort(Protocol):
    pepper: str = "lol123"
    salt_len: int = 5
    def encode(self, text: str, salt: str) -> str: ...
    def verify(self, text: str, salt: str, hashed_text: str) -> bool: ...
    @property
    def salt(self) -> str: ...
