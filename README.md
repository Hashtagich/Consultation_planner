# Consultation_planner

## Запуск проекта
___

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Hashtagich/Consultation_planner.git
```

2. Запускаем backend

    2.1. Установите и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    venv/Scripts/activate  - для Windows
    venv/bin/activate - для Linux
    ```

    2.2 Перейдите в папку backend и установите зависимости:
    ```bash
    cd backend
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    2.3 Находясь в папке backend выполните миграции:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
    
    2.4 Находясь в папке backend создайте суперпользователя:
    ```bash
    python manage.py createsuperuser
    ```
    
    2.5 Находясь в папке backend запустите проект:
    ```bash
    python manage.py runserver
    ```

___

### API

<font color="red">Информация может быть изменена</font>

***Страница с документацией по API***

<code>http://127.0.0.1:8000/api/v1/swagger/</code>

***API Регистрация и логирование***
<details>
<summary><code>POST/api/v1/auth/users/</code></summary>



*Регистрация пользователя. Необходимо ввести почту и пароль. Пароль должен быть не менее 8 символов и содержать минимум одну строчную латинскую букву и цифры.*

```
{
  "email": "user@example.com",
  "password": "string",
  "re_password": "string"
}
```

</details>
<details>
<summary><code>POST/api/v1/auth/jwt/create/</code></summary>

*Логирование пользователя и генерация токена. Необходимо ввести почту и пароль пользователя.*

```
{
  "email": "string",
  "password": "string"
}
```

</details>
<details>
<summary><code>GET/api/ссылка_на_апи/</code></summary>

*Описание API*

```
Код
```

</details>