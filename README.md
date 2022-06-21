# Foodgram

![example workflow](https://github.com/shdrn2402/foodgram-project-react/workflows/foodgram_workflow/badge.svg)  
  
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Подготовка и запуск проекта локально

## Склонировать репозиторий на локальную машину
* git clone <https://github.com/shdrn2402/foodgram-project-react>

* Cоздайте .env файл в директории backend/foodgram/fodgram/ и впишите:

```python
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    POSTGRES_USER=<пользователь бд>
    POSTGRES_PASSWORD=<пароль>
    DB_HOST=db
    DB_PORT=<5432>
    DJANGO_SECRET_KEY=<секретный ключ проекта django>
    DJANGO_DEBUG=1
```

* перейдите в директорию infra/

* выполните команду  sudo docker-compose up

* Выполните миграции:

```python
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
```

* создайте суперпользователя

sudo docker-compose exec backend python manage.py createsuperuser

* Для наполнения тестовыми рецептами и пользователями данными используйте комманду:

```python
sudo docker-compose exec backend python manage.py loaddata foodgram_db.json
```

Наполнение ингредиентов осуществляется за счёт библиотеки django-import-export через админ панель.
Перейдите в админ панель в модель ингредиентов и укажите файл ingredients.json, который находится в корне проекта foodgram/data/, для импорта, после чего подтвердите импорт - confirm.

* Админ-панель проекта доступна по адресу

```python
http://127.0.0.1:8000/admin
```

* Проект доступен по адресу

```python
http://127.0.0.1:8000
```

* Развертывание проекта на удаленном сервере:

* Выполните вход на свой удаленный сервер

* Установите docker на сервер:

```python
sudo apt install docker.io 
```

* Установите docker-compose на сервер:

```python
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

* Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой своего сервера

* Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:

```python
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx/default.conf
```

* Скопируйте тестовые данные из директории backend/foodgram/data/foodgram_db.json:

```python
scp foodgram_db.json <username>@<host>:/home/<username>/foodgram_db.json
```

* Cоздайте .env файл и впишите:

    ```python
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    DJANGO_SECRET_KEY=<секретный ключ проекта django>
    DJANGO_DEBUG=1
    ```

* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:

    ```python
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>
    
    DJANGO_SECRET_KEY=<секретный ключ проекта django>

    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

    TELEGRAM_TO=<ID чата, в который придет сообщение>
    TELEGRAM_TOKEN=<токен вашего бота>
    ```

    Workflow состоит из трёх шагов:

    ```python
     - Проверка кода на соответствие PEP8
     - Сборка и публикация образа бекенда на DockerHub.
     - Автоматический деплой на удаленный сервер.
     - Отправка уведомления в телеграм-чат.  
    ```

* На сервере соберите docker-compose:

```python
sudo docker-compose up -d --build
```

* После успешной сборки на сервере выполните команды (только после первого деплоя):

Соберите статические файлы:

```python
sudo docker-compose exec backend python manage.py collectstatic --noinput
```

Примените миграции:

```python
sudo docker-compose exec backend python manage.py migrate --noinput
```

Создать суперпользователя Django:

```python
sudo docker-compose exec backend python manage.py createsuperuser
```

Проект будет доступен по вашему IP. Наполнение базы тестовыми данными описано выше.

## Проект в интернете

* Проект запущен и доступен по [адресу](http://bestrecipes.ddns.net/recipes)

* Admin - панель доступна по [адресу](http://bestrecipes.ddns.net/admin)

* логин/email/пароль суперпользователя: admin/admin@fake.ru/234WERsdf