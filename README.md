# Новостной портал

Мультиязычный новостной портал с поддержкой аутентификации и чатом с ботом.

## Функциональность

- Мультиязычность (русский, английский, казахский)
- Аутентификация и авторизация пользователей
- Новостной портал с категориями
- Поиск статей
- Чат с ботом (для авторизованных пользователей)
- Темная/светлая тема

## Технологии

- Django 5.1.4
- Bootstrap 5.3.0
- SQLite (для разработки) / PostgreSQL (для продакшена)
- Django i18n для мультиязычности

## Локальная установка

1. Клонируйте репозиторий:
```
git clone https://github.com/yourusername/lab4.git
cd lab4
```

2. Создайте виртуальное окружение и активируйте его:
```
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```
pip install -r requirements.txt
```

4. Создайте файл .env на основе .env.example:
```
cp .env.example .env
```

5. Отредактируйте файл .env, указав необходимые параметры.

6. Примените миграции:
```
python manage.py migrate
```

7. Создайте суперпользователя:
```
python manage.py createsuperuser
```

8. Скомпилируйте файлы перевода:
```
python manage.py compilemessages
```

9. Запустите сервер разработки:
```
python manage.py runserver
```

10. Откройте http://127.0.0.1:8000/ в браузере.

## Развертывание на Heroku

1. Установите [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

2. Войдите в свой аккаунт Heroku:
```
heroku login
```

3. Создайте новое приложение:
```
heroku create your-app-name
```

4. Добавьте PostgreSQL:
```
heroku addons:create heroku-postgresql:mini
```

5. Настройте переменные окружения:
```
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

6. Отправьте код на Heroku:
```
git push heroku main
```

7. Примените миграции:
```
heroku run python manage.py migrate
```

8. Создайте суперпользователя:
```
heroku run python manage.py createsuperuser
```

9. Откройте приложение:
```
heroku open
```

## Развертывание на других платформах

### PythonAnywhere

1. Загрузите код на PythonAnywhere.
2. Создайте виртуальное окружение и установите зависимости.
3. Настройте WSGI-файл.
4. Настройте статические файлы.
5. Перезапустите приложение.

### DigitalOcean

1. Создайте Droplet с Ubuntu.
2. Установите необходимые пакеты (Python, Nginx, Gunicorn).
3. Загрузите код на сервер.
4. Настройте Nginx и Gunicorn.
5. Запустите приложение.

## Лицензия

MIT 