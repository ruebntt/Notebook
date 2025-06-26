# Ежедневник (Backend API)

Это REST API для приложения-ежедневника, реализованное с помощью FastAPI и PostgreSQL. API предоставляет все CRUD операции для работы с записями, а также возможность помечать запись выполненной.

## Технологии
- Python 3.11+
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- Alembic (для миграций)

## Установка

1. Клонируйте репозиторий 
```bash
git clone https://github.com/ваш-аккаунт/daily-planner.git
cd daily-planner

Создайте виртуальное окружение и активируйте его
CopyRun
python -m venv env
source env/bin/activate  # Linux/Mac
.\env\Scripts\activate   # Windows

3. Установите зависимости
CopyRun
pip install -r requirements.txt

4. Настройте базу данных PostgreSQL и создайте базу данных, например, daily_planner. Обновите файл .env с вашими данными.

5. Выполните миграции Alembic для создания таблиц

CopyRun
alembic upgrade head

Создание записи (EntryCreate)
CopyRun
{
  "title": "Название задачи",
  "description": "Описание задачи",
  "date": "2024-04-27"
}

Обновление записи (EntryUpdate)
CopyRun
{
  "title": "Новое название",
  "description": "Новое описание",
  "date": "2024-04-28"
}
