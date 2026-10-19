# Менеджер задач

Учебный проект Django. Python 3.11 или 3.12, Django 5.2, SQLite, django-bootstrap4.

## Запуск на Windows (PowerShell)
Откройте терминал PyCharm в папке **task_manager**, где лежит `manage.py`.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py test
python manage.py runserver 8000
```

Если PowerShell не разрешает активацию, выполните команды через `.venv\Scripts\python.exe` вместо `python` (без активации).
Сайт: http://127.0.0.1:8000/

Для административной панели создайте пользователя:
```powershell
python manage.py createsuperuser
```
Затем откройте http://127.0.0.1:8000/admin/.

## Docker Compose
Установите Docker Desktop. В папке проекта скопируйте `.env.example` в `.env` и замените `DJANGO_SECRET_KEY` на длинную случайную строку.

```powershell
Copy-Item .env.example .env
docker compose up -d --build
docker compose exec web python manage.py test
docker compose exec web python manage.py createsuperuser
```

Сайт: http://127.0.0.1:8000/. Остановить: `docker compose down`.
SQLite хранится в именованном томе `sqlite_data` и сохраняется после перезапуска контейнера. Не используйте `docker compose down -v`, если хотите сохранить данные.

## Настройка сервера
В `.env` укажите `DJANGO_DEBUG=0`, уникальный `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS=IP_СЕРВЕРА,localhost,127.0.0.1`.
Если работаете через HTTPS-прокси, задайте `DJANGO_CSRF_TRUSTED_ORIGINS=https://ваш-домен` и `DJANGO_USE_HTTPS=1`. Порт наружу меняется переменной `APP_PORT` (по умолчанию 8000).
Никогда не публикуйте файл `.env` и базу с персональными данными.

## Тесты
`python manage.py check` и `python manage.py test` (локально) или `docker compose exec web python manage.py test`.

## Структура
- `task_manager/` — настройки и основные маршруты Django
- `tasks/models.py` — модель предметной области
- `tasks/forms.py` — форма ModelForm
- `tasks/views.py` — представления, проверка прав
- `tasks/urls.py` — адреса страниц
- `tasks/templates/` — HTML и Bootstrap 4
- `users/` — регистрация, вход и выход
- `tasks/tests.py` — автоматические тесты
- `compose.yaml`, `Dockerfile` — контейнеризация

# TaskManager
# TaskManager
