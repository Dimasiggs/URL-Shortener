# Simple URL shortener
Сервис коротких ссылок с аналитикой — это полноценный проект для тренировки архитектуры, с аутентификацией, доменной логикой, инфраструктурой и статистикой.

## Обзор проекта

Пользователи регистрируются, создают короткие ссылки на свои URL, получают статистику по кликам. Админы видят глобальную аналитику и управляют блоклистом. [roadmap](https://roadmap.sh/backend/project-ideas)
Фокус на backend: clean/onion архитектура, SOLID, PostgreSQL + Alembic. [pypi](https://pypi.org/project/fast-clean-architecture/)
Фронтенд: только Swagger + 1 простая HTML-страница для создания ссылки и просмотра своей статистики (fetch + таблица).

## Сущности домена

- **User**: id, email, hashed_password, role (user/admin), created_at. [roadmap](https://roadmap.sh/backend/project-ideas)
- **Link**: id, short_code (уникальный, 6–8 символов), original_url, owner_user_id, custom_slug (опционально), is_active, created_at, expires_at (опционально). [roadmap](https://roadmap.sh/backend/project-ideas)
- **Click**: id, link_id, ip_address, user_agent, referrer (опционально), country (опционально, заглушка по IP), created_at (timestamp клика). [roadmap](https://roadmap.sh/backend/project-ideas)
- **BlockedDomain**: domain (для админов), reason, is_active (чтобы блокировать подозрительные ссылки). [roadmap](https://roadmap.sh/backend/project-ideas)

## Бизнес-логика и правила

- Генерация short_code: случайная строка (base62), уникальная, проверка коллизий. [roadmap](https://roadmap.sh/backend/project-ideas)
- Кастомный slug: пользователь может задать свой, но уникальный среди его ссылок. [roadmap](https://roadmap.sh/backend/project-ideas)
- Валидация URL: must be valid http/https, не из блоклиста. [roadmap](https://roadmap.sh/backend/project-ideas)
- Статистика: total clicks, unique IPs, топ-страны, график кликов по дням (group by date). [roadmap](https://roadmap.sh/backend/project-ideas)
- Роли: user видит только свои ссылки/статистику; admin — все + блоклист. [roadmap](https://roadmap.sh/backend/project-ideas)

## API эндпоинты

Все защищены JWT кроме /auth и GET /{short_code}.

### Аутентификация
- `POST /auth/register` — {email, password} → user_id, access_token. [projectpro](https://www.projectpro.io/article/fastapi-projects/847)
- `POST /auth/login` — {email, password} → access_token. [projectpro](https://www.projectpro.io/article/fastapi-projects/847)
- `GET /auth/me` — текущий user info. [projectpro](https://www.projectpro.io/article/fastapi-projects/847)

### Ссылки (user)
- `POST /links` — {original_url, custom_slug?, expires_at?} → {short_url, link_id}. [roadmap](https://roadmap.sh/backend/project-ideas)
- `GET /links` — ?page, ?limit → список своих ссылок (paginated). [roadmap](https://roadmap.sh/backend/project-ideas)
- `GET /links/{id}` — детали ссылки. [roadmap](https://roadmap.sh/backend/project-ideas)
- `DELETE /links/{id}` — удалить свою. [roadmap](https://roadmap.sh/backend/project-ideas)

### Статистика (user)
- `GET /links/{id}/stats` — ?from_date, ?to_date → {total_clicks, unique_ips, top_countries: [...], clicks_per_day: [...]}. [roadmap](https://roadmap.sh/backend/project-ideas)
- `GET /links/{id}/clicks` — ?page, ?limit → список кликов (paginated). [roadmap](https://roadmap.sh/backend/project-ideas)

### Редирект (public)
- `GET /{short_code}` — redirect to original_url, лог клика (async). [roadmap](https://roadmap.sh/backend/project-ideas)

### Админ
- `GET /admin/links` — все ссылки (paginated). [roadmap](https://roadmap.sh/backend/project-ideas)
- `GET /admin/stats/global` — общая статистика (total_links, total_clicks и т.д.). [roadmap](https://roadmap.sh/backend/project-ideas)
- `POST /admin/blocked-domains` — {domain, reason}. [roadmap](https://roadmap.sh/backend/project-ideas)
- `GET /admin/blocked-domains` — список. [roadmap](https://roadmap.sh/backend/project-ideas)

## Архитектура (Clean/Onion)

### Domain layer
- Entities: User, Link, Click, BlockedDomain (Pydantic BaseModel или dataclasses). [github](https://github.com/bodaue/fastapi-clean-architecture)
- Value Objects: ShortCode (с генерацией/валидацией), Url (валидация). [pypi](https://pypi.org/project/fast-clean-architecture/)
- Domain Services: LinkShortener (генерация кода, проверка уникальности). [pypi](https://pypi.org/project/fast-clean-architecture/)

### Application layer (Use Cases)
- CreateLinkUseCase(user_id, original_url, custom_slug?, expires_at?) → LinkId.  
- GetLinkStatsUseCase(link_id, user_id?, from_date?, to_date?) → StatsDto.  
- ResolveLinkUseCase(short_code) → original_url + log_click async.  
- BlockDomainUseCase(domain, reason) — только admin. [github](https://github.com/bodaue/fastapi-clean-architecture)
Каждый use case — класс с __call__, принимает DTO, вызывает репозитории через протоколы. [pypi](https://pypi.org/project/fast-clean-architecture/)

### Infrastructure
- Repositories (протоколы): UserRepository, LinkRepository, ClickRepository, BlockedDomainRepository. [github](https://github.com/bodaue/fastapi-clean-architecture)
- Реализации: SQLAlchemyRepository (async session).
- External: JWTService, PasswordHasher (bcrypt/argon2), UrlValidator, IpToCountry (заглушка или free API). [projectpro](https://www.projectpro.io/article/fastapi-projects/847)
- Кэш: Redis для short_code → link_id (чтобы редирект был быстрым). [projectpro](https://www.projectpro.io/article/fastapi-projects/847)

### Presentation (FastAPI)
- Dependencies: get_current_user (из JWT). [projectpro](https://www.projectpro.io/article/fastapi-projects/847)
- Роутеры: auth_router, links_router, stats_router, admin_router. [projectpro](https://www.projectpro.io/article/fastapi-projects/847)
- BackgroundTasks для логирования кликов (не блокировать редирект). [roadmap](https://roadmap.sh/backend/project-ideas)

## База данных (PostgreSQL)

Таблицы (миграции Alembic):

```sql
users: id (uuid), email (unique), hashed_password, role (enum), created_at.
links: id (uuid), short_code (varchar unique), original_url (text), owner_id (fk users), custom_slug, is_active (bool), expires_at (timestamp?), created_at.
clicks: id (uuid), link_id (fk links), ip_address, user_agent (text), referrer (text), country (varchar), created_at (timestamp).
blocked_domains: id (uuid), domain (unique), reason (text), is_active (bool).
```

Индексы: short_code (unique), links.owner_id, clicks.link_id + created_at (для stats), clicks.ip_address (partial для unique).

## Фронтенд (минимальный)

- index.html: форма логина/регистрации, поле для URL → кнопка “сократить”, таблица своих ссылок + кнопка “статистика”. [realpython](https://realpython.com/fastapi-python-web-apis/)
- JS: fetch к API, localStorage для токена, простая таблица. Без React/Alpine.  
- Всё остальное — Swagger на /docs для теста/админки.

## Структура проекта

```
project/
├── app/
│   ├── domain/          # entities, value objects, domain services
│   ├── application/     # use cases
│   ├── infrastructure/  # repositories impl, services (jwt, hasher)
│   ├── presentation/    # routers, dependencies, schemas pydantic
│   ├── core/            # config, exceptions
├── migrations/          # alembic
├── docker-compose.yml   # postgres + redis
├── static/              # index.html + style.css
└── main.py
```

## Запуск и деплой

- Docker: postgres, redis, app.
- Env: DATABASE_URL, SECRET_KEY, REDIS_URL. [projectpro](https://www.projectpro.io/article/fastapi-projects/847)
- Миграции: alembic upgrade head.
- Тесты: pytest для unit (use cases + mocks), integration (API). [github](https://github.com/bodaue/fastapi-clean-architecture)
