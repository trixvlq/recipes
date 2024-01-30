# Тестовое задание

**Стек:**

![Python](https://img.shields.io/badge/Python-4169E1?style=for-the-badge)
![Django](https://img.shields.io/badge/Django-008000?style=for-the-badge)
![DRF](https://img.shields.io/badge/DRF-800000?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-00BFFF?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-87CEEB?style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

# Описание проекта

Этот проект представляет собой решение тестового задания от MirGovorit.

Сайт обладает следующим функционалом:
- Просмотр рецептов
- Их изменение
- Фильтрация рецептов по ингредиенту

# Как запустить проект

1. Клонировать репозиторий:



```
https://github.com/trixvlq/recipes.git
```

2. Создать Docker контейнер:

```
docker-compose build
```

3. Создать миграции:

```
docker-compose run --rm recepies_app sh -c "python manage.py makemigrations"
docker-compose run --rm recepies_app sh -c "python manage.py migrate"
```

4. Создать админа:

```
docker-compose run --rm recepies_app sh -c "python manage.py createsuperuser"
```

5. Запустить контейнер:

```
docker-compose up
```

Теперь проект доступен по адресу:

```
http://127.0.0.1/
```