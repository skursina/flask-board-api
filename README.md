# Flask Board API

REST API для сервиса объявлений на Flask.

Проект выполнен в рамках учебного задания по созданию REST API, авторизации пользователей, работе с PostgreSQL, Docker и CI/CD.

## Возможности

API позволяет:

- регистрировать пользователей;
- авторизовываться с помощью JWT;
- создавать объявления;
- получать объявление по ID;
- редактировать свои объявления;
- удалять свои объявления;
- ограничивать создание объявлений только авторизованными пользователями;
- ограничивать редактирование и удаление только владельцем объявления.

## Стек

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- PostgreSQL 16
- Gunicorn
- Docker
- Docker Compose
- Pytest
- GitHub Actions

## Структура проекта

```text
flask-board-api/
├── app/
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
│
├── tests/
│   └── ...
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Модели данных
### User

Пользователь содержит:

* `id`
* `email`
* `password_hash`

Пароль хранится не в открытом виде, а в виде хеша.

### Advertisement

Объявление содержит:

* `id`
* `title`
* `description`
* `created_at`
* `owner_id`

`owner_id` связывает объявление с пользователем, который его создал.

## API

Базовый URL:

```
http://localhost:5000
```
При запуске на сервере:

```
http://SERVER_IP:5000
```

### Проверка работы API

```http
GET /
```
Ответ:
```json
{
  "message": "Flask API работает"
}
```

### Регистрация пользователя
```http
POST /register
Content-Type: application/json
```
Пример:
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```
Ответ:
```json
{
  "id": 1,
  "message": "user created"
}
```

### Авторизация
```http
POST /login
Content-Type: application/json
```
Пример:
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```
Ответ:
```json
{
  "access_token": "JWT_TOKEN"
}
```

Полученный JWT используется для доступа к защищённым endpoint'ам.

Заголовок запроса:
```
Authorization: Bearer JWT_TOKEN
```

### Создание объявления

Создавать объявления могут только авторизованные пользователи.

```http
POST /ads
Authorization: Bearer JWT_TOKEN
Content-Type: application/json
```
Пример:
```bash
curl -X POST http://localhost:5000/ads \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer JWT_TOKEN" \
  -d '{"title":"Новое объявление","description":"Описание объявления"}'
```
Ответ:
```json
{
  "id": 1,
  "message": "Объявление добавлено"
}
```
Без JWT API возвращает:
```http
401 Unauthorized
```
### Получение объявления
```http
GET /ads/<id>
```
Пример:
```bash
curl http://localhost:5000/ads/1
```
Ответ:
```json
{
  "id": 1,
  "title": "Новое объявление",
  "description": "Описание объявления",
  "created_at": "2026-09-08T19:38:05.296406",
  "owner": "test@example.com"
}
```
Получение объявления не требует авторизации.

### Редактирование объявления

Редактировать объявление может только его владелец.
```http
PUT /ads/<id>
Authorization: Bearer JWT_TOKEN
Content-Type: application/json
```
Пример:
```bash
curl -X PUT http://localhost:5000/ads/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer JWT_TOKEN" \
  -d '{"title":"Изменённый заголовок"}'
```
Ответ:
```json
{
  "id": 1,
  "message": "Объявление обновлено!"
}
```
Если пользователь не является владельцем:
```http
403 Forbidden
```
### Удаление объявления

Удалять объявление может только его владелец.
```http
DELETE /ads/<id>
Authorization: Bearer JWT_TOKEN
```
Пример:
```bash
curl -X DELETE http://localhost:5000/ads/1 \
  -H "Authorization: Bearer JWT_TOKEN"
```
Ответ:
```json
{
  "message": "advertisement deleted"
}
```
После удаления получение объявления возвращает:
```http
404 Not Found
```

## Запуск проекта локально
### 1. Клонирование репозитория
```bash
git clone https://github.com/skursina/flask-board-api.git
cd flask-board-api
```

### 2. Создание виртуального окружения

Linux / WSL:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создать файл `.env`:

```
DATABASE_URL=postgresql://flask_user:flask_password@localhost:5432/flask_ads_db
SECRET_KEY=your-secret-key
```
Файл `.env` не должен добавляться в Git.

### 5. Запуск PostgreSQL

Для локального запуска PostgreSQL можно использовать Docker:
```bash
docker compose up -d postgres
```

### 6. Запуск Flask
```bash
flask --app app run
```
API будет доступен по адресу:
```http
http://localhost:5000
```

## Запуск через Docker Compose

Проект содержит `Dockerfile` и `docker-compose.yml`.

Запуск:
```bash
docker compose up -d --build
```
Проверка контейнеров:
```bash
docker compose ps
```
Просмотр логов:
```bash
docker compose logs web
```
Остановка:
```bash
docker compose down
```
После запуска API доступен:
```http
http://localhost:5000
```
PostgreSQL внутри Docker работает на стандартном порту:
```
5432
```

## Тестирование

Для запуска тестов:
```
pytest
```
В проекте тестируется основная функциональность API:
* регистрация пользователя;
* авторизация;
* создание объявления;
* получение объявления;
* изменение объявления;
* удаление объявления;
* запрет создания без авторизации;
* запрет изменения чужого объявления;
* обработка отсутствующего объявления.

## CI/CD

Для проекта настроен GitHub Actions workflow:
```
.github/workflows/ci-cd.yml
```
При каждом push в ветку main выполняется:
```
Git push
    ↓
GitHub Actions
    ↓
Запуск PostgreSQL
    ↓
Установка зависимостей
    ↓
pytest
    ↓
Deploy на сервер
    ↓
git pull
    ↓
docker compose up -d --build
    ↓
Healthcheck
    ↓
Application healthy
```
При `pull request` выполняются тесты.

При успешном `push` в `main` выполняется автоматический деплой на сервер.

### Healthcheck

После запуска контейнера CI/CD проверяет состояние Flask-контейнера.

Если контейнер становится:
```
healthy
```
деплой считается успешным.

Если приложение становится:
```
unhealthy
```
GitHub Actions выводит логи контейнера и завершает workflow с ошибкой.

## Деплой на сервер

Приложение развёрнуто на Linux-сервере с использованием Docker Compose.

На сервере используются два контейнера:
```
flask_ads_api
flask_ads_postgres
```
Схема работы:
```
Client
   ↓
Gunicorn
   ↓
Flask API
   ↓
SQLAlchemy
   ↓
PostgreSQL
```
Деплой выполняется автоматически через GitHub Actions.

После изменения кода достаточно выполнить:
```bash
git add .
git commit -m "Update application"
git push origin main
```
После успешного прохождения тестов GitHub Actions самостоятельно обновляет приложение на сервере.

## Переменные окружения

Используются следующие переменные:

|Переменная	|Назначение|
|-----------|----------|
|`DATABASE_URL`|	URL подключения к PostgreSQL|
|`SECRET_KEY`| секретный ключ приложения и JWT|

Секретные значения не хранятся в репозитории.

Для GitHub Actions используются GitHub Secrets:

* `SERVER_HOST`
* `SERVER_USER`
* `SSH_PRIVATE_KEY`
* `SERVER_PATH`

## Проверка выполненного задания

Реализованы требования задания:

### REST API
- [ x ] создание объявления;
- [ x ] получение объявления;
- [ x ] изменение объявления;
- [ x ] удаление объявления;
- [ x ] дата создания;
- [ x ] владелец объявления.
### Авторизация и права
- [ x ] регистрация пользователя;
- [ x ] хранение пароля в виде хеша;
- [ x ] JWT-аутентификация;
- [ x ] создание объявления только авторизованным пользователем;
- [ x ] изменение объявления только владельцем;
- [ x ] удаление объявления только владельцем;
- [ x ] запрет доступа к операциям без авторизации.
### Инфраструктура
- [ x ] PostgreSQL;
- [ x ] Docker;
- [ x ] Docker Compose;
- [ x ] Gunicorn;
- [ x ] GitHub Actions;
- [ x ] автоматический деплой;
- [ x ] healthcheck приложения.