# Auth - 2
Ссылка на репозиторий - https://github.com/lppavli/Auth_sprint_2

Добавлена возможность регистрации и аутенитификации с помощью Google и Yandex-аккаунтов.
# Запуск приложения
```
docker-compose up -d- --build 
```
# Миграции
```
docker exec -it auth cd auth && alembic upgrade head
```
# Документация доступна по адресу
http://127.0.0.1/apidocs/
# Создание суперпользователя
```
docker exec -it auth cd auth && flask superuser create <login> <email> <password>
```
# Тестирование
```
docker-compose -f docker-compose-test.yml up -d- --build
```