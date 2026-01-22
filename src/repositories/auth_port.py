from typing import Protocol

class AuthRepositoryPort(Protocol):
    async def login(): ...

