# ArticleHub API

REST API для роботи з користувачами та статтями, створений на **Django + Django REST Framework**.

Проєкт підтримує JWT-авторизацію, MongoDB, асинхронні задачі через Celery, Redis та автоматичну документацію Swagger.

---

## Технології

| Компонент        | Технологія                      |
| ---------------- | ------------------------------- |
| Backend          | Django 5, Django REST Framework |
| Database         | MongoDB + MongoEngine           |
| Authentication   | JWT (SimpleJWT)                 |
| Background Tasks | Celery + Redis                  |
| Documentation    | Swagger UI                      |
| Package Manager  | uv                              |
| Testing          | pytest, pytest-cov              |
| CI/CD            | GitHub Actions                  |
| Deployment       | Docker, AWS EC2                 |

---

# Функціонал

* Реєстрація та авторизація користувачів
* JWT authentication
* Перегляд профілю користувача
* CRUD операції зі статтями
* Пошук статей
* Фільтрація за тегами
* Аналіз статей через Celery
* Welcome Email task (лог)
* Щоденна статистика через Celery Beat
* Swagger документація
* Автоматичне тестування
* CI/CD через GitHub Actions
* Deploy на AWS EC2

---

# Вимоги

* Python 3.12+
* Docker Desktop
* uv

Встановлення `uv`:

```bash
pip install uv
```

---

# Встановлення

Клонування репозиторію:

```bash
git clone <repository-url>
cd article-hub-api
```

Встановлення залежностей:

```bash
uv sync
```

Створення `.env`:

```bash
cp .env.example .env
```

Приклад конфігурації:

```env
SECRET_KEY=dev-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

MONGODB_URI=mongodb://localhost:27017/articlehub

REDIS_URL=redis://localhost:6379/0

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

# Запуск MongoDB та Redis

## Docker

MongoDB:

```bash
docker run -d --name articlehub-mongo -p 27017:27017 mongo:7
```

Redis:

```bash
docker run -d --name articlehub-redis -p 6379:6379 redis:7
```

Або через Docker Compose:

```bash
docker compose up mongo redis -d
```

Перевірка запущених контейнерів:

```bash
docker ps
```

---

# Запуск проєкту

Потрібно відкрити 3 термінали.

## Django сервер

```bash
uv run python manage.py migrate
uv run python manage.py runserver
```

API:

```text
http://127.0.0.1:8000/
```

Swagger:

```text
http://127.0.0.1:8000/api/docs/
```

---

## Celery Worker

Для Windows:

```bash
uv run celery -A config worker -l info -P solo
```

---

## Celery Beat

```bash
uv run celery -A config beat -l info
```

---

# API Endpoints

## Authentication

### Реєстрація

```text
POST /api/auth/register/
```

Body:

```json
{
  "email": "user@example.com",
  "password": "string123",
  "name": "John Doe"
}
```

Після успішної реєстрації Celery Worker виведе:

```text
Welcome email sent to user@example.com
```

---

### Авторизація

```text
POST /api/auth/login/
```

Body:

```json
{
  "email": "user@example.com",
  "password": "string123"
}
```

Response:

```json
{
  "access": "...",
  "refresh": "..."
}
```

---

### Профіль

```text
GET /api/auth/profile/
```

Header:

```text
Authorization: Bearer <access_token>
```

---

# Articles

## Створення статті

```text
POST /api/articles/
```

Body:

```json
{
  "title": "My first article",
  "content": "Some text",
  "tags": [
    "python",
    "django"
  ]
}
```

---

## Отримати список статей

```text
GET /api/articles/
```

---

## Пошук

```text
GET /api/articles/?search=first
```

---

## Фільтр за тегом

```text
GET /api/articles/?tag=python
```

---

## Детальна інформація

```text
GET /api/articles/{id}/
```

---

## Оновлення

```text
PUT /api/articles/{id}/
```

Доступно тільки автору.

---

## Видалення

```text
DELETE /api/articles/{id}/
```

Доступно тільки автору.

---

# Celery Tasks

## Аналіз статті

Запуск:

```text
POST /api/articles/{id}/analyze/
```

Response:

```text
202 Accepted
```

Приклад результату:

```json
{
  "analysis": {
    "word_count": 250,
    "unique_tags": 4
  }
}
```

---

## Daily Statistics

Celery Beat запускає задачу щодня о 00:00 UTC.

Для тестування можна тимчасово змінити:

```python
crontab(minute="*/1")
```

У логах:

```text
Daily article stats: total_articles=...
```

---

# Перевірка через PowerShell

## Register

```powershell
Invoke-RestMethod `
-Uri "http://127.0.0.1:8000/api/auth/register/" `
-Method POST `
-ContentType "application/json" `
-Body '{"email":"user@example.com","password":"string123","name":"John Doe"}'
```

---

## Login

```powershell
$t = (Invoke-RestMethod `
-Uri "http://127.0.0.1:8000/api/auth/login/" `
-Method POST `
-ContentType "application/json" `
-Body '{"email":"user@example.com","password":"string123"}').access
```

---

## Profile

```powershell
Invoke-RestMethod `
-Uri "http://127.0.0.1:8000/api/auth/profile/" `
-Headers @{Authorization="Bearer $t"}
```

---

## Create Article

```powershell
$a = Invoke-RestMethod `
-Uri "http://127.0.0.1:8000/api/articles/" `
-Method POST `
-Headers @{Authorization="Bearer $t"} `
-ContentType "application/json" `
-Body '{"title":"My article","content":"Text","tags":["python"]}'
```

---

## Analyze Article

```powershell
Invoke-RestMethod `
-Uri "http://127.0.0.1:8000/api/articles/$($a.id)/analyze/" `
-Method POST `
-Headers @{Authorization="Bearer $t"}
```

---

# Структура проєкту

```text
article-hub-api/

├── articles/             # Articles CRUD
├── users/                # Authentication
├── tasks/                # Celery tasks
├── config/               # Django settings, URLs, MongoDB, Celery
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── articles/
│   │   │   ├── test_models.py
│   │   │   ├── test_serializers.py
│   │   │   └── test_views.py
│   │   ├── users/
│   │   │   ├── test_authentication.py
│   │   │   ├── test_models.py
│   │   │   ├── test_serializers.py
│   │   │   └── test_views.py
│   │   └── tasks/
│   │       └── test_tasks.py
│   ├── integrational/
│   │   └── test_integration.py
│   └── test_external_services.py
├── manage.py
├── pyproject.toml
└── .env
```

---

# Тести

Проєкт використовує **pytest** для автоматизованого тестування.

## Що тестується

Тестове покриття включає:

* моделі користувачів та статей;
* serializers та валідацію даних;
* API views;
* JWT authentication;
* CRUD операції зі статтями;
* пошук та фільтрацію;
* Celery tasks;
* інтеграційні сценарії;
* зовнішні сервіси за допомогою mocks.

## Структура тестів

### Unit tests

```text
tests/unit/
├── articles/
│   ├── test_models.py
│   ├── test_serializers.py
│   └── test_views.py
├── users/
│   ├── test_authentication.py
│   ├── test_models.py
│   ├── test_serializers.py
│   └── test_views.py
└── tasks/
    └── test_tasks.py
```

### Integration tests

```text
tests/integrational/
└── test_integration.py
```

Інтеграційні тести перевіряють взаємодію декількох компонентів системи в межах одного сценарію.

### External services

```text
tests/test_external_services.py
```

Тести зовнішніх сервісів використовують mocks, щоб ізолювати тестований код від реальних зовнішніх запитів.

---

## Запуск тестів

Запустити всі тести:

```bash
uv run pytest -v
```

Запустити unit tests:

```bash
uv run pytest -v tests/unit/
```

Запустити integration tests:

```bash
uv run pytest -v tests/integrational/
```

Запустити тести конкретного модуля:

```bash
uv run pytest -v tests/unit/articles/
uv run pytest -v tests/unit/users/
```

Запустити конкретний файл:

```bash
uv run pytest -v tests/unit/articles/test_models.py
```

---

## Coverage

Перевірити покриття коду:

```bash
uv run pytest \
  --cov=articles \
  --cov=users \
  --cov=tasks \
  --cov-report=term-missing
```

Створити HTML-звіт:

```bash
uv run pytest \
  --cov=articles \
  --cov=users \
  --cov=tasks \
  --cov-report=html
```

HTML-звіт буде доступний у:

```text
htmlcov/index.html
```

---

# CI/CD

GitHub Actions workflow знаходиться у:

```text
.github/workflows/ci.yml
```

Workflow запускається:

* при `push` у `main` або `master`;
* при створенні або оновленні Pull Request.

## Test job

CI автоматично:

1. Checkout репозиторію;
2. запускає MongoDB 7;
3. запускає Redis 7;
4. встановлює Python 3.12;
5. встановлює залежності через `uv sync`;
6. запускає `pytest`;
7. перевіряє code coverage;
8. зберігає coverage report як artifact.

## Deploy job

Deploy залежить від успішного завершення test job.

Після успішних тестів при `push` у `main` виконується:

```text
GitHub Actions
      ↓
Tests
      ↓
Coverage
      ↓
SSH → AWS EC2
      ↓
git pull
      ↓
docker compose up -d --build
```

Результати виконання workflow можна переглянути у вкладці **Actions** репозиторію на GitHub.

---

# Troubleshooting

| Проблема                 | Рішення                             |
| ------------------------ | ----------------------------------- |
| MongoDB connection error | Перевірити `docker ps`              |
| Celery не запускається   | Перевірити Redis на порту 6379      |
| Welcome Email не працює  | Запустити Celery Worker             |
| Analyze не працює        | Перевірити Worker та Redis          |
| 401 Unauthorized         | Додати JWT Bearer token             |
| 403 Forbidden            | Операцію може виконати тільки автор |

---

# Очистити MongoDB

```bash
docker exec -it articlehub-mongo mongosh articlehub --eval "db.users.drop(); db.articles.drop()"
```

---

# Зупинити контейнери

```bash
docker stop articlehub-mongo articlehub-redis
```

---

# Deploy on AWS EC2

## 1. EC2

Ubuntu instance з відкритими портами:

* `22` — SSH
* `80` — HTTP
* `443` — HTTPS

## 2. Docker

Встановити Docker, Docker Compose Plugin та Git:

```bash
sudo apt install docker.io docker-compose-plugin git
```

## 3. MongoDB Atlas

Створити MongoDB Atlas cluster та додати URI у `.env`:

```env
MONGODB_URI=mongodb+srv://USER:PASSWORD@cluster.mongodb.net/articlehub?retryWrites=true&w=majority

ALLOWED_HOSTS=your-domain.com,EC2_IP

DEBUG=False
```

## 4. Запуск на сервері

```bash
git clone <repository-url>

cd article-hub-api

cp .env.example .env
```

Відредагувати `.env` та запустити:

```bash
docker compose up -d --build
```

Застосувати міграції:

```bash
docker compose exec web python manage.py migrate
```

## 5. Nginx + HTTPS

Встановити Nginx та Certbot:

```bash
sudo apt install certbot python3-certbot-nginx
```

Nginx працює як reverse proxy на `web:8000`.

Отримати SSL-сертифікат:

```bash
sudo certbot --nginx -d your-domain.com
```

API буде доступне за адресою:

```text
https://your-domain.com/api/docs/
```
