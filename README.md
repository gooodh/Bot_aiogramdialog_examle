# Telegram Bot Template for Aiogram 3 + SQLAlchemy

This project is a comprehensive template for the development of scalable Telegram bots using the Aiogram 3 framework, SQLAlchemy for working with the database, and Alembic for migration management.

The convenient `loguru` library is used for logging. Thanks to this, the logs are beautifully highlighted in the console and recorded in the log file in the background.

## Technology Stack

- **Telegram API**: Aiogram 3
- **ORM**: SQLAlchemy with aiosqlite
- **Database**: SQLite
- **Migration System**: Alembic

## Architecture Overview

The project follows an architecture inspired by microservices and FastAPI best practices. Each functional component of the bot is organized as a mini-service, which ensures modularity of development and maintenance.

## Project Structure
```
├── bot/
│   ├── migration/
│   │   ├── versions
│   │   ├── env.py
│   ├── dao/
│   │   ├── base.py
│   ├── users/
│   │   ├── keyboards/
│   │   │ ├── inline_kb.py
│   │   │ ├── markup_kb.py
│   │   ├── models.py
│   │   ├── utils.py
│   │   └── router.py
│   ├── database.py
│   ├── log.txt
│   ├── main.py
│   └── config.py
├── data/
│   ├── db.sqlite3
├── alembic.ini
├── .env
├── docker-compose.yml
└── requirements.txt
```

## Environment Variables

Create a file named `.env` at the root of the project with the following content:
```
BOT_TOKEN=your_bot_token_here
PORT=8080
HOST=0.0.0.0
BASE_URL=https://######.duckdns.org
ADMIN_IDS=[12345,344334]
POSTGRES_USER=postgres_container
POSTGRES_PASSWORD=postgres_container
POSTGRES_HOST=172.18.0.2
POSTGRES_PORT=5432
POSTGRES_DB=postgres
```


## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:gooodh/AiogramAlchemyTemp.git
   cd your-repo-name

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    Set up the database:
4. Postgres and pgadmin start in docker:
   ```bash
   docker compose up -d --build
6. Run migrations using Alembic:
    ```bash

    alembic upgrade head

