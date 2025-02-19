## Тест 1: Получить объявление по ID

### Цель: Проверить возможность получения объявления по ID.

## Шаги: 

1. Создать новое объявление с помощью POST-запроса.

2. Отправить GET-запрос на URL `https://qa-internship.avito.com/api/1/item/:id` с полученным `id`.

## Ожидаемый результат:

1. Статус ответа — 200 для валидного id.

2. В теле ответа id совпадает с переданным.

3. Структура ответа соответствует ожидаемому JSON.

## Проверка:

### Проверка валидности ID:

- Для валидного `id` - статус 200.
- Для невалидного `id` (None, "@#$%", -10, " ") - статус 400.
- Для несуществующего `id` - статус 404.

### Проверка структуры JSON:

- Ответ для валидного id должен содержать:

```json
[{
    "id": "<string>",
    "sellerId": "<integer>",
    "name": "<string>",
    "price": "<integer>",
    "statistics": {
        "likes": "<integer>",
        "viewCount": "<integer>",
        "contacts": "<integer>"
    },
    "createdAt": "<string>"
}]
```
- Для несуществующего id ответ должен содержать:

```json
{
    "result": {
        "messages": {},
        "message": "<string>"
    },
    "status": "<string>"
}
```

## Тест 2: Получить все объявления по продавцам

### Цель: Проверить возможность получения списка всех объявлений для определенного продавца.

## Шаги: 

1. Отправить GET-запрос на URL `https://qa-internship.avito.com/api/1/:sellerID/item` с корректным `sellerID`.

2. Сравнить `sellerID` из запроса с `sellerId` каждого объявления в ответе.

## Ожидаемый результат:

1. Статус ответа - 200 для валидного `sellerID`.

2. Все объявления должны содержать соответствующий `sellerId`.

3. Структура ответа соответствует ожидаемому JSON.

## Проверка:

### Проверка валидности sellerID:

- Для валидного `sellerID` - статус 200.
- Для невалидного `sellerID` ("", None, отрицательные числа, @#$%) — статус 400.

### Проверка структуры JSON:

- Ответ для валидного `sellerID` должен содержать:

```json
[{
    "id": "<string>",
    "sellerId": "<integer>",
    "name": "<string>",
    "price": "<integer>",
    "statistics": {
        "likes": "<integer>",
        "viewCount": "<integer>",
        "contacts": "<integer>"
    },
    "createdAt": "<string>"
}]
```
- Для невалидного `sellerID` ответ должен содержать:

```json
{
    "result": {
        "messages": {},
        "message": "<string>"
    },
    "status": "<string>"
}
```

## Тест 3: Получить статистику по ID

### Цель: Проверить возможность получения статистики для объявления по ID.

## Шаги: 

1. Создать новое объявление с помощью POST-запроса.

2. Извлечь `id` созданного объявления.

3. Отправить GET-запрос на URL `https://qa-internship.avito.com/api/1/statistic/:id` с полученным `id`.

## Ожидаемый результат:

1. Статус-код ответа - 200 для валидного `id`.

2. Статистика в ответе должна совпадать с данными, полученными через GET запрос на объявление.

## Проверка:

### Проверка валидности ID:

- Для валидного `id` — статус 200.
- Для невалидного `id` (строка, None, отрицательные числа, @#$%) - статус 400
- Для несуществующего `id` - статус 404.

### Проверка структуры JSON:

- Ответ для валидного `id` должен содержать:

```json
[{
    "likes": "<integer>",
    "viewCount": "<integer>",
    "contacts": "<integer>"
}]
```
- Для несуществующего `id` ответ должен содержать:

```json
{
    "result": {
        "messages": {},
        "message": "<string>"
    },
    "status": "<string>"
}
```

## Тест 4: Сохранить объявление

### Цель: Проверить возможность создания нового объявления.

## Шаги: 

1. Отправить POST-запрос с JSON-данными объявления.

2. Получить ответ с `status`.

3. Проверить создание нового объявления через GET-запрос с ID.

## Ожидаемый результат:

1. Ответ от сервера содержит статус создания.

2. Запрос на GET для созданного объявления возвращает корректные данные.

## Проверка:

### Проверка структуры ответа:

- Ответ на POST-запрос должен содержать:

```json
{
    "status": "<string>"
}

```

### Проверка невалидных данных:

- В случае передачи невалидных данных (sellerID, price = 0 / none и т.д) - сервер должен вернуть статус 400. 

### Проверка структуры данных при сохранении:

- Ответ на запрос создания объявления с некорректными данными (Неверный тип для name или price) должен содержать:

```json
{
    "result": {
        "messages": {
            "nostrudffb": "<string>",
            "Ut__": "<string>"
        },
        "message": "<string>"
    },
    "status": "<string>"
}

```