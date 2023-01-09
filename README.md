# Проект YaMDb
![main_workflow](https://github.com/Petro2561/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


Проект "YaMDb" собирает отзывы пользователей на произведения.
Сами произведения в "YaMDb" не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку.
На основе пользовательских оценок формируется усреднённая оценка произведения — рейтинг.

Проект подготовлен для изучения базовых принципов построения
API на основе фреймворка [DRF]

## Примеры работы с api проекта:

Получение списка произведений

```
GET api/v1/titles/
```

Получение списка отзывов на произведение

```
 GET api/v1/titles/{title_id}/reviews/
```

Получение списка комментариев к отзывам

```
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

Подробное описание api в формате ReDoc доступно [тут]

[DRF]: <https://www.django-rest-framework.org/>
[тут]: http://localhost/redoc/

## Запуск проекта на удаленном сервере.
Для запуска проекта необходимо:
- скачать Docker https://docs.docker.com/get-docker/
- клонировать репозитарий git clone https://github.com/Petro2561/yamdb_final.git
- cоздать .env и заполнить по образцу:
   - DB_ENGINE=django.db.backends.postgresql
   - DB_NAME=postgres
   - POSTGRES_USER=postgres
   - POSTGRES_PASSWORD=<придумайте пароль>
   - DB_HOST=db
   - DB_PORT=5432
   - SECRET_KEY=<ключ в одинарных ковычках>
- запустить проект docker-compose up -d
- выполнить миграции командой docker-compose exec web python manage.py migrate
- создать суперпользователя docker-compose exec web python manage.py createsuperuser
- собрать статику docker-compose exec web python manage.py collectstatic
- проект готов к запуску, http://localhost/admin/ можно перейти в админку

