## Deliveery

Delivery это проект для заказа доставки грузов. ,
AngularJS-powered HTML5 Markdown editor.

- Type some Markdown on the left
- See HTML in the right
- ✨Magic ✨

## Функции

Создание клиентом накладных в PDF файл со следующими параметрами:
- Описание груза
- Вес груза
- Габариты груза
- Точный адрес отправки
- Точный адрес получения
- Способ оплаты

Регистрация претензии со следующими параметрами:

- номер накладной
- e-mail для ответа на претензию
- описание ситуации
- требуемая сумма
- фото/сканы

## Технологии

- [Python] - язык программирования!
- [Asyncio] - модуль для организации конкурентного программирования.
- [Aiogram] - Библиотека для разработки ботов.
- [Docker] - это платформа для разработки, доставки и запуска контейнерных приложений.

## Переменные окружения

```
BOT_TOKEN=
MANAGER=
```

## Установка и запуск

Delivery зависит [Python.](https://python.org/) v3+ to run.

```sh
cd delivery
pip install -r requirements.txt
python main.py
```

## Docker

Delivery очень легко учстановить и развернуть в Docker container.

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

```sh
cd dillinger
docker build -t <youruser>/delivery:${package.json.version} .
```

