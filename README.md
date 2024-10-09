# Сервис планирования консультаций в рамках стажировки в компании Promo-IT.

<details>
<summary>

## Описание сервиса
</summary>
Backend приложение, которое позволяет Клиентам планировать консультации с различными Специалистами.

</details>

---
<details>
<summary>

## Описание функционала
</summary>

1) Регистрация в роли Клиента или Специалиста;
2) Специалисты могут:
* просматривать своё расписание;
* соглашаться или отказываться с датой проведения консультации, что зарезервировал Клиент, при этому приходит уведомление на эл. почту Клиента;
* создавать слоты консультаций, причём нельзя создать слот с одинаковыми специалистами и датами начала - окончания.
3) Клиенты могут:
* выбирать свободный слот для консультации;
* до того как Специалист согласовал консультацию, Клиент может отказаться от консультации и написать комментарий, при этому приходит уведомление на эл. почту Специалисту;
* видеть только зарезервированные собой и свободные консультации;
4) Администраторы могу:
* заблокировать или разблокировать пользователя;
* получить список всех пользователей;
* редактировать данные пользователей.

</details>

---
<details>
<summary>

## Запуск проекта
</summary>

### 1. Клонирование репозиторий
```bash
git clone https://github.com/Hashtagich/Consultation_planner.git
```

### 2. Установка переменных окружения
***В корен проекта заполняем файл template.db.env и переименовываем его в db.env или просто создаём файл db.env и заполняем его***
```bash
POSTGRES_DB=Например, db
POSTGRES_USER=Например, db
POSTGRES_PASSWORD=Например, db
```

***В папке backend заполняем файл template.env и переименовываем его в .env или просто создаём файл .env и заполняем его***
 ```bash
 SECRET_KEY='Ваш секретный ключ проекта'
 DEBUG=Булевое значение True или False
 ALLOWED_HOSTS='Разрешенные хосты'
 LANGUAGE_CODE='Язык, например, ru'
 TIME_ZONE='Временная зона, например, UTC'

 DB_NAME='Имя Базы данных (БД), например, db'
 DB_LOGIN='Логин БД, например, db'
 DB_PASS='Пароль БД, например, db'
 DB_HOST='Хост БД, например, db'
 DB_PORT='Порт БД, например, 5432'
 
 EMAIL_BACKEND='Сервис для почты, например, django.core.mail.backends.smtp.EmailBackend'
 EMAIL_HOST='Хост почты, например для gmail smtp.gmail.com или smtp.mail.ru для mail'
 EMAIL_PORT=Порт почты, например, 587
 DEFAULT_FROM_EMAIL='Почта с которой будет отправлять письма youremail@gmail.com если выбрали smtp.gmail.com'
 EMAIL_USE_TLS=Булевое значение True или False причём EMAIL_USE_TLS не равен EMAIL_USE_SSL
 EMAIL_USE_SSL=Булевое значение True или False причём EMAIL_USE_TLS не равен EMAIL_USE_SSL
 EMAIL_HOST_PASSWORD='Пароль для внешнего приложения для доступа к почте, подробнее тут https://help.mail.ru/mail/security/protection/external/'
 NOTIFICATION_EMAIL='Перечень почт куда будут отправлять письма, пишите через пробел, можно указать одну'

 CELERY_BROKER_URL='URL-адрес брокера сообщений, например,redis://localhost:6379'
 CELERY_RESULT_BACKEND='Место хранения результатов выполнения задач, например,redis://localhost:6379'
 CELERY_ACCEPT_CONTENT='Список форматов, которые Celery будет принимать в качестве контента для задач, например,application/json'
 CELERY_TASK_SERIALIZER='Сериализатор, который будет использоваться для сериализации задач перед их отправкой, например,json'
 CELERY_RESULT_SERIALIZER='Сериализатор, который будет использоваться для сериализации результатов задач, например,json'
 ```

### 3. Сборка и запуск контейнеров
```bash
docker-compose up --build -d
```

### 4. Инициализация БД (Создание ролей для пользователей)
```bash
docker-compose exec web python manage.py initialize_db
```

### 5. Создание суперпользователя. Для роли Администратора указать id роли 1.
```bash
docker-compose exec web python manage.py createsuperuser
```

</details>

___

### Urls и API

***Административная панель***

<code>/admin/</code>

***Страница с документацией по API***

<code>/api/v1/swagger/</code>

***API Регистрация и логирование***
<details>
<summary><code>POST/api/v1/register/</code></summary>

*Регистрация пользователя. Необходимо ввести фамилию, имя, отчество, роль, почту и пароль. Пароль должен быть не менее 8 символов и содержать минимум одну строчную латинскую букву и цифры.*

```
{
  "first_name": "string",
  "last_name": "string",
  "middle_name": "string",
  "email": "user@example.com",
  "role": 0,
  "password": "string"
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

***API для Администратора***
<details>
<summary><code>GET/api/v1/users/</code></summary>

*Получение списка всех пользователей*
```
[
  {
    "id": 0,
    "first_name": "string",
    "last_name": "string",
    "middle_name": "string",
    "role": "",
    "phone": "string",
    "email": "user@example.com",
    "is_staff": true,
    "is_active": true,
    "is_blocked": true
  }
]
```
</details>
<details>
<summary><code>GET/api/v1/users/{id}/</code></summary>

*Получение информации о пользователе через его id*

```
{
  "id": 0,
  "first_name": "string",
  "last_name": "string",
  "middle_name": "string",
  "role": "",
  "phone": "string",
  "email": "user@example.com",
  "is_staff": true,
  "is_active": true,
  "is_blocked": true
}
```

</details>
<details>
<summary><code>PATCH/api/v1/users/{id}/</code></summary>

*Редактирования конкретного пользователя по ID*

```
{
  "first_name": "string",
  "last_name": "string",
  "middle_name": "string",
  "role": 0,
  "is_staff": true,
  "is_active": true,
  "is_blocked": true
}
```

</details>
<details>
<summary><code>PATCH/api/v1/users/{id}/unblock_user/</code></summary>

*Разблокировка пользователя*

</details>
<details>
<summary><code>PATCH/api/v1/users/{id}/block_user/</code></summary>

*Блокировка пользователя*

</details>


***API для Клиентов и Специалистов***
<details>
<summary><code>GET/api/v1/slots/</code></summary>

*Получение всех слотов, для каждой роли свои слоты, сортировка по статусам*

```
[
  {
    "specialist": 0,
    "start_time": "2024-10-08T17:41:48.229Z",
    "end_time": "2024-10-08T17:41:48.229Z",
    "context": "string",
    "cost": "35.",
    "status": "free",
    "client": 0
  }
]
```

</details>
<details>
<summary><code>GET/api/v1/slots/{id}/</code></summary>

*Получение слота по id, для каждой роли свой слот, сортировка по статусу*

```
{
  "specialist": 0,
  "start_time": "2024-10-08T17:42:00.697Z",
  "end_time": "2024-10-08T17:42:00.697Z",
  "context": "string",
  "cost": "295",
  "status": "free",
  "client": 0
}
```

</details>

***API для Специалиста***

<details>
<summary><code>POST/api/v1/slots/</code></summary>

*Создание слота*

```
{
  "start_time": "2024-10-08T17:11:51.489Z",
  "end_time": "2024-10-08T17:11:51.489Z",
  "context": "string",
  "cost": "93"
}
```

</details>
<details>
<summary><code>PATCH/api/v1/slots/{id}/</code></summary>

*Редактирование слота*

```
{
  "start_time": "2024-10-08T17:29:06.627Z",
  "end_time": "2024-10-08T17:29:06.627Z",
  "context": "string",
  "cost": "-719"
}
```

</details>
<details>
<summary><code>DELETE/api/v1/slots/{id}/</code></summary>

*Удаление слота*

</details>
<details>
<summary><code>PATCH/api/v1/slots/{id}/agree/</code></summary>

*Согласование слота, который зарезервировал Клиент, Специалистом и отправка письма-уведомления Клиенту*
</details>
<details>
<summary><code>PATCH/api/v1/slots/{id}/cancel_specialist/</code></summary>

*Отказ в согласовании слота, который зарезервировал Клиент, Специалистом и отправка письма-уведомления Клиенту*

</details>

***API для Клиента***
<details>
<summary><code>PATCH/api/v1/slots/{id}/reserve/</code></summary>

*Резервирование слота Клиентом*

</details>
<details>
<summary><code>PATCH/api/v1/slots/{id}/cancel_client/</code></summary>

*Отмена резервирования слота Клиентом и написание комментария. Поля client и slot заполняется автоматически и указывается текущий слот и Клиент, text необязательное поле, reason выбирается из списка, в случаи не заполнения будет причина "Форс-мажор"*

```
{
  "reason": "None",
  "text": "string",
  "client": 0,
  "slot": 0
}
```

</details>
