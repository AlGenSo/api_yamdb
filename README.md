**Проект «YaMDb»**
---
---
### Описание
##### Идея проекта
Проект YaMDb собирает отзывы пользователей на произведения.
Здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
##### Задача проекта
Написать бэкенд проекта (приложение **reviews**) и **AP**I для него (приложение **api**)
##### Ресурсы API YaMDb

- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
---
### Технологии:
- Django 
- Django REST Framework
- Django Filter
- PyJWT
---
### Установка
##### Требования для корректной работы
[python 3.7](https://www.python.org/downloads/), django 3.2
##### Для тестирования запросов можно использовать
[Postman](https://www.postman.com/downloads/)
### Запуск проекта
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/AlGenSo/api_yamdb.git
```
```
cd api_yamdb
```
---
Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
```
source env/bin/activate
```
```
python3 -m pip install --upgrade pip
```
---
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
---

---
### Примеры. 
##### Некоторые примеры запросов к API.
_Когда вы запустите проект, по адресу http://127.0.0.1:8000/redoc/ будет доступна документация проекта YaMDb._
|Описание|Запрос|Тип|Результат|Body|
|:----:|:----:|:----:|:----:|:----:|
|AUTH|`api/v1/auth/signup/`|POST|Регистрация нового пользователя.|`{"email": "string", "username": "string"}`|
|AUTH|`api/v1/auth/token/`|POST|Получение JWT-токена.|`{"username": "string", "confirmation_code": "string"}`|
|GENRES|`api/v1/genres/`|POST|Добавление жанра.|`{"name": "string", "slug": "string"}`|
|TITLES|`api/v1/titles/{titles_id}/`|GET|Получение информации о произведении.|`{"id": 0, "name": "string", "year": 0,  "rating": 0, "description": "string", "genre": [{"name": "string", "slug": "string"}], "category": {"name": "string",   "slug": "string"}}`|
|REVIEWS|`api/v1/titles/{title_id}/reviews/{review_id}//`|GET|Полуение отзыва по id.|`{"id": 0, "text": "string",  "author": "string", "score": 1, "pub_date": "2019-08-24T14:15:22Z"}`|
|COMMENTS|`api/v1/titles/{title_id}/reviews/{review_id}/comments/`|DEL|Добавление комментария к отзыву.|`{"text":"string"}`|
|USERS|`api/v1/users/{username}/`|PATCH|Изменение данных пользователя по username.|`{"username": "string",<br/> "email":"user@example.com", "first_name": "string", "last_name": "string", "bio": "string", "role": "user"}`|
|USERS|`api/v1/users/{username}/`|DEL|Удаление пользователя по username.|`----`|
---
---
### Команда разработчиков:
- Кондаков Тимофей
- Сенгилейцев Никита
- Солодовников Александр (по совместительству тимлид)
---
