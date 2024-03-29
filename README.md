# Финальный проект спринта: «API для Yatube»

## Описание

API для Yatube представляет собой проект разработки программного интерфейса (API) для социальной сети Yatube, в которой реализованы возможности публиковать записи, комментировать их, а так же подписываться или отписываться от авторов.

## Стек технологий

* Python 3.9,
* Django 3.2,
* Django REST Framework 3.12,
* JWT + Djoser

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:tsromych/api_final_yatube.git
```
```bash
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv env
```
```bash
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
cd yatube_api
```
```bash
python3 manage.py migrate
```

Запустить проект:

```bash
python3 manage.py runserver
```

## Документация к API проекта:
### Примеры работы с API для всех пользователей

Для неавторизованных пользователей работа с API доступна только в режиме чтения, создание и изменение контента запрещено.

```r
GET api/v1/posts/ - получить список всех публикаций.
При указании параметров limit и offset выдача должна работать с пагинацией
GET api/v1/posts/{id}/ - получение публикации по id
GET api/v1/groups/ - получение списка доступных сообществ
GET api/v1/groups/{id}/ - получение информации о сообществе по id
GET api/v1/{post_id}/comments/ - получение всех комментариев к публикации
GET api/v1/{post_id}/comments/{id}/ - Получение комментария к публикации по id
```

### Примеры работы с API для авторизованных пользователей

Авторизованные пользователи могут создавать посты, комментировать их и подписываться на других пользователей. Пользователи могут изменять (удалять) контент, автором которого они являются.

Для создания публикации используем:

```r
POST /api/v1/posts/
```

в запросе передаем:

```json
{
"text": "string",
"image": "string",
"group": 0
}
```

Обновление публикации:

```r
PUT /api/v1/posts/{id}/
```

в запросе передаем:

```json
{
"text": "string",
"image": "string",
"group": 0
}
```

Удаление публикации:

```r
DEL /api/v1/posts/{id}/
```

Получение доступа к эндпоинту /api/v1/follow/ (подписки) доступен только для авторизованных пользователей.
