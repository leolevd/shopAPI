# Shop API


## Возможности User
Получить список уникальных товаров – каждый товар в единичном экземпляре, у него есть описание, название и цена.
`GET /api/goods`
```json
{
    "111": {"name": "Water", "description": "Bottle 0.5L", "price": "0.99"},
    "141": {"name": "Cheesecake", "description": "1000g", "price": "25.30"}
}
```

Показать корзину

`GET /api/basket/<basketid>`

Добавить товар в корзину

`POST /api/basket/`

Удалить товар из корзины

`DELETE /api/basket/`

Оформить заказ. Чтобы это сделать пользователю достаточно указать свою почту.

`POST /api/order/<email>`

## Возможности Manager
Изменять характеристики товаров

`PUT /api/goods/<id>`
Authentication i835987398 <-- Login:password in base64

## Возможности Admin

Изменять характеристики товаров

`PUT /api/goods/<id>`

Добавлять товары

`POST /api/goods/<id>`

Удалять товары

`DELETE /api/goods/<id>`

-----------------

## Хранение

1. Goods
```json
{
    "1": {"name": "Coca-Cola", "description": "1.5L", "price": 3.5}
}
```
2. Orders
```json
{
    {"status": 0, "in": ["3", "2", "5"], "email": "eee@mail.com"}
}
```
3. Users
```json
{
    {"username": "Larry", "password": "yenodes", "role": "MANAGER"},
    {"username": "Liova", "password": "nofods", "role": "ADMIN"}
}
```
