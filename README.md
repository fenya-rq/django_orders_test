# Тестовое задание на Django 2.2+

Допускается использование сторонних библиотек и плагинов.  
Структура и архитектура проекта, типы полей на ваше усмотрение.  
Прислать ссылку на репозиторий с проектом (гитхаб/гитлаб/…).
___
## Часть 1

Создать модели с полями. Вынести их в админ-панель.

### Модели:

#### Товар:
- Название
- Картинка
- Контент
- Стоимость

#### Заказ:
- Итоговая сумма
- Статус
- Время создания
- Время подтверждения

#### Платеж:
- Сумма
- Статус
- Тип оплаты

___
## Часть 2

Создать эндпоинты.

### Эндпоинты:

#### 1. Эндпоинт получения списка Товаров:
- **GET-запрос** с выдачей списка Товаров.

#### 2. Эндпоинт создания нового Заказа:
- **POST-запрос** с указанием списка Товаров. 
- Итоговая сумма Заказа должна складываться из стоимостей всех Товаров.
- Во время создания должен записываться текущий таймстамп.

#### 3. Эндпоинт создания нового Платежа:
- **POST-запрос** с указанием Заказа.
- Сумма должна браться из итоговой суммы Заказа.
- 
___
## Часть 3

Добавить в админке к модели Заказ кнопку подтверждения заказа.  
Она должна отображаться только если связанный Платеж имеет статус “Оплачен”.  
При нажатии на кнопку нужно изменить статус Заказа на “Подтвержден”, сохранить текущую дату и время в поле Время подтверждения.  
Сымитировать подготовку заказа (можно просто через `sleep` на несколько секунд) и отправить **POST-запрос** по адресу `https://webhook.site/36693e00-8f59-4f7b-9a85-1d1e7ddde4d4` с телом JSON:  

```json
{
  "id": ИД_ЗАКАЗА,
  "amount": СУММА_ЗАКАЗА,
  "date": ВРЕМЯ_ПОДТВЕРЖДЕНИЯ
}
```
___

## Инструкция по развёртыванию:

Для работы необходимо иметь установленный Poetry.
https://python-poetry.org/docs/#installing-with-the-official-installer

Скачиваем репозиторий в нужную директорию:

    git clone https://github.com/fenya-rq/django_orders_test.git
Переходим:

    cd django_orders_test
Устанавливаем зависимости и активируем окружение:

    poetry install
    poetry shell
Переходим:

    cd django_orders/django_orders
В этой директории необходимо создать **.env** файл, скопировать содержимое файла **.env.dist**
и указать свои данные для подключения к БД.

После переходим в директорию с **manage.py**:
    
    cd ..
И применяем миграции:

    poetry run python manage.py migrate
После чего создаем пользователя-админа:

    poetry run python manage.py createsuperuser
Если хотим иметь немного моковых данных в БД - загружаем фикстуры:

    poetry run python manage.py loaddata products orders orderitems payments
Запуск тестов и выдача процента покрытия тестами:

    poetry run pytest
Запускаем сервер:

    poetry run python manage.py runserver