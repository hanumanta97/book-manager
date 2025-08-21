# Book Manager — Django REST API (InsideAIML Assignment)

A clean, containerized Django REST API for managing Books. Uses **PostgreSQL**, **Django REST Framework**, and **Docker** (with optional `docker-compose`).

## Quick Start (Docker)

```bash
# 1) Clone the repo
git clone https://github.com/hanumanta97/book-manager.git
cd book_manager

# 2) (Optional) copy env
cp .env.sample .env

# 3) Build & run
docker-compose up --build
# API will be available at http://localhost:8000/api/books/
```

To stop:
```bash
docker-compose down
```

## Local Dev (without Docker)

Requires Python 3.11+ and PostgreSQL running locally.

```bash
python -m venv venv  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export DEBUG=1
export SECRET_KEY=dev-secret
export POSTGRES_DB=book_manager
export POSTGRES_USER=book_user
export POSTGRES_PASSWORD=book_pass
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

-- Connect to PostgreSQL as the default user
psql -U postgres

-- Create database
CREATE DATABASE book_manager;

-- Create user
CREATE USER book_user WITH PASSWORD 'book_pass';

-- Grant privileges on schema
GRANT ALL PRIVILEGES ON SCHEMA public TO book_user;
ALTER SCHEMA public OWNER TO book_user;

-- Allow the user to create databases if needed
ALTER USER book_user CREATEDB;
```
## API Endpoints

Base path: `/api/`

- `POST   /api/books/` — Create a book
- `GET    /api/books/` — List books (supports filters, pagination)
- `GET    /api/books/{id}/` — Retrieve a book
- `PUT    /api/books/{id}/` — Update a book
- `PATCH  /api/books/{id}/` — Partial update
- `DELETE /api/books/{id}/` — Delete a book
- *(Bonus)* `POST /api/token-auth/` — Obtain Token (if you enable token auth)

### Filters (Bonus)

- `/api/books/?author=Rowling`
- `/api/books/?is_available=true`
- `/api/books/?search=harry` (searches title/author)
- `/api/books/?ordering=-published_date,title` (ordering by fields)
- Pagination: `/api/books/?page=2&page_size=5` (page size configurable)

## Curl Examples

```bash
# Create
curl -X POST http://localhost:8000/api/books/   -H "Content-Type: application/json"   -d '{"title":"Clean Architecture","author":"Robert C. Martin","published_date":"2017-09-20","is_available":true}'

# List
curl http://localhost:8000/api/books/

# Retrieve
curl http://localhost:8000/api/books/1/

# Update
curl -X PUT http://localhost:8000/api/books/1/   -H "Content-Type: application/json"   -d '{"title":"Clean Architecture (Updated)","author":"Robert Martin","published_date":"2018-01-01","is_available":false}'

# Delete
curl -X DELETE http://localhost:8000/api/books/1/

# Token (optional)
curl -X POST http://localhost:8000/api/token-auth/   -H "Content-Type: application/json"   -d '{"username":"admin","password":"adminpass"}'
```

## Project Structure

```
book_manager/
├─ book_manager/        # Project settings
├─ books/               # App (model, serializer, viewset, urls, tests)
├─ manage.py
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
└─ README.md
```

## Running Tests (Bonus)

```bash
pytest  # if you add pytest, or:
python manage.py test
```

## Notes

- Default auth is open (`AllowAny`) so reviewers can hit the API immediately.
- Token auth is wired and can be enforced by switching default permission to `IsAuthenticated`.
- Uses `django-filter` for clean filtering.
