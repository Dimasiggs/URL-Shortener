"""Все роутеры API приложения."""

# from api.v1.user import router as router_users
from src.api.v1.auth import router as router_auth
from src.api.v1.link import router as router_links

all_routers = [
    router_links,
    router_auth,
]
