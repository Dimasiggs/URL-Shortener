# Simple URL shortener
Сервис коротких ссылок с аналитикой — это полноценный проект для тренировки архитектуры, с аутентификацией, доменной логикой, инфраструктурой и статистикой.

## Обзор проекта

Пользователи регистрируются, создают короткие ссылки на свои URL, получают статистику по кликам. Админы видят глобальную аналитику и управляют блоклистом.
Фокус на backend: clean/onion архитектура, SOLID, PostgreSQL + Alembic.
Фронтенд: только Swagger + 1 простая HTML-страница для создания ссылки и просмотра своей статистики (fetch + таблица).


## Сущности домена

- **User**: id, nickname, hashed_password, salt, role (user/admin), created_at.
- **Link**: id, short_code (уникальный, 6–8 символов), original_url, owner_user_id, custom_slug (опционально), is_active, created_at, expires_at (опционально).
- **Click**: id, link_id, ip_address, user_agent, referrer (опционально), country (опционально, заглушка по IP), created_at (timestamp клика).
- **BlockedDomain**: domain (для админов), reason, is_active (чтобы блокировать подозрительные ссылки).


### Аутентификация
- `POST /auth/register` — {nickname, password} → user_id, access_token. 
- `POST /auth/login` — {nickname, password} → access_token. 
- `GET /auth/me` — текущий user info. 

### Ссылки (user)
- `POST /links` — {original_url, custom_slug?, expires_at?} → {short_url, link_id}. 
- `GET /links` — ?page, ?limit → список своих ссылок (paginated). 
- `GET /links/{id}/stats` — детали ссылки. 
- `DELETE /links/{id}` — удалить свою. 

### Статистика (user)
- `GET /links/{id}/stats` — ?from_date, ?to_date → {total_clicks, unique_ips, top_countries: [...], clicks_per_day: [...]}. 
- `GET /links/{id}/clicks` — ?page, ?limit → список кликов (paginated). 

### Редирект (public)
- `GET /r/{short_code}` — redirect to original_url, лог клика (async). 

### Админ
- `GET /admin/links` — все ссылки (paginated). 
- `GET /admin/stats/global` — общая статистика (total_links, total_clicks и т.д.). 
- `POST /admin/blocked-domains` — {domain, reason}. 
- `GET /admin/blocked-domains` — список. 



## Запуск и деплой
- Замените параметры в файле .env на свои
- Запустите контейнер командой: ``` docker compose up --build ```
- Сайт откроется на [http:/localhost:8000/index.html](http://localhost:8000/index.html)
- Сваггер откроется на [http:/localhost:8000/docs](http://localhost:8000/docs)


# Список задач:
### 01. 
### 02. Реализовать вывод статистики по каждой ссылке
### 03. Сделать возможность задавать собственный короткий код для ссылок
### 04. Сделать срок действия ссылок
### 05. Сделать суперпользователя, который будет видеть все созданные ссылки
### 06. Рефакторинг (Сделать нормальные Exceptions)
### 07. Рефакторинг (Разобраться с функциями в репозиториях, которые делают почти одно и то же)
### 08. Сделать модель кликов для бд
### 09. Добавлять в бд клики и информацию о них


# Сделанные задачи:
### 01. Добавить проверку пароля при авторизации
### 02. Добавлять клики при переходе по короткой ссылке
### 03. Сделать реальную аутентификацию, а не заглушку
### 04. Реализовать удаление ссылок
### 05. Убрать заглушку имени пользователя в `/api/v1/auth/me`
### 06. Убрать заглушку в `/api/v1/register`
### 07. Рефакторинг (разобраться со схемами)


# Планы/идеи на будущее:
### 01. Автотесты
### 02. Kubernetes
### 03. Микросервисы/gRPC
### 04. Redis
### 05. CI/CD
### 06. ...