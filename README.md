# Тестовое задание

## Реализовано:
- Модель пользователя с полями (usename, email, баланс, ставка комиссии, URL webhook и роль)
- Модель транзакции с полями (сумма, комиссия, статус, дата создания, опционально id пользователя)
- CLI команда для создания дефолтного админа - `flask main_routes.admin_cli create-admin`
- Создана админка с тремя вкладками
- Созданы эндпоинты для создания, отмены и проверки транзакции
- Сделана Swagger документация - доступна по адресу - `http://127.0.0.1:5000/api/docs/`
- Сделана Сelery задача , которая каждую минуту проверяет транзакции со статусом Ожидание и если прошло более 15 минут меняет статус на Истекла и отправляет вебхук на URL webhook
  (вебхук реализован черезх эндпоинт в котором происходит print присланного JSON, так как в ТЗ не уточнялись подробности вебхука)
  Celery задача реализована без дополнительных инструментов, чтобы не перегружать задание
  Для запуска Celery таски нужно в двух отдельных терминалах выполнить команды:
  
  `celery -A tasks.celery worker --loglevel=info --pool=solo`
  
  `celery -A tasks.celery beat --loglevel=info`
  
- В админку добавлен фильтр для транзакций по id пользователя и статусу транзакции
- В админке учтены особенности наличия ролей Пользователя, админу доступно все. Обычный пользователь видит только свои транзакции.


## Эндпоинты
Создание транзакции - `http://127.0.0.1:5000/create_transaction`

Отмена транзакции - `http://127.0.0.1:5000/cancel_transaction`

Проверка транзакции - `http://127.0.0.1:5000/check_transaction/<id>`

Создание пользователя - `http://127.0.0.1:5000/create_user`

Также реализован HTML шаблон для логина пользователя по адресу - `http://127.0.0.1:5000/login`

Эндпоинт для логаута - `http://127.0.0.1:5000/logout`
