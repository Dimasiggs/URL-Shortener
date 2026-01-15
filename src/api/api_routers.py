"""Все роутеры API приложения."""

# from api.v1.user import router as router_users
from src.api.v1.auth import router as router_auth

all_routers = [
    # router_users,
    router_auth,
]
