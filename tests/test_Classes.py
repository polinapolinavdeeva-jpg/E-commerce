import pytest

from src.Classes import Category, Iterator, LawnGrass, Product, Smartphone


def test_product_init(product):
    assert product.name == "Samsung S 25"
    assert product.description == "Лучший выбор"
    assert product.price == 120999.99
    assert product.quantity == 16


def test_category_init(category):
    assert category.name == "Смартфон"
    assert category.description == "Флагманы 2026"
    assert len(category.products.splitlines()) == 3


def test_category_count():
    Category.category_count = 0
    product_4 = Product("Ariston", "Мороз по коже", 25000, 5)
    product_5 = Product("LG", "Генератор снега", 31999, 8)
    p_list_2 = [product_4, product_5]

    product_6 = Product("Молоток", "Сделано в СССР", 3560, 56)
    product_7 = Product("Пила", "Зубчатая", 1590, 49)
    p_list_3 = [product_6, product_7]

    Category("Бытовая техника", "Для кухни", p_list_2)
    Category("Инструмент", "Для дома", p_list_3)
    assert Category.category_count == 2


def test_product_count():
    Category.product_count = 0
    product_4 = Product("Ariston", "Мороз по коже", 25000, 5)
    product_5 = Product("LG", "Генератор снега", 31999, 8)
    p_list_2 = [product_4, product_5]

    product_6 = Product("Молоток", "Сделано в СССР", 3560, 56)
    product_7 = Product("Пила", "Зубчатая", 1590, 49)
    p_list_3 = [product_6, product_7]

    Category("Бытовая техника", "Для кухни", p_list_2)
    Category("Инструмент", "Для дома", p_list_3)
    assert Category.product_count == 4


def test_add_product():
    category = Category("Телефоны", "Смартфоны", [])
    product = Product("iPhone", "Apple", 100000, 5)

    category.add_product(product)

    assert "iPhone, 100000 руб. Остаток: 5 шт.\n" in category.products


def test_counter_add_product():
    Category.product_count = 0
    category = Category("название", "описание", [])
    new_product = Product("iPhone", "Apple", 100000, 5)
    category.add_product(new_product)
    assert Category.product_count == 1


def test_add():
    category = Category("Название_1", "Описание_1", [])
    product = Product("Фон", "Яблоко", 200000, 3)
    category.add_product(product)
    assert category.products == "Фон, 200000 руб. Остаток: 3 шт.\n"


def test_new_product():
    product_data = {
        "name": "Товар",
        "description": "Хороший",
        "price": 100,
        "quantity": 2,
    }

    existing_data = []

    result = Product.new_product(product_data, existing_data)

    assert isinstance(result, Product)
    assert result.name == product_data["name"]
    assert result.description == product_data["description"]
    assert result.price == product_data["price"]
    assert result.quantity == product_data["quantity"]


def test_new_product_duplicate():
    existing_product = Product("Мопс", "Красивый", 100, 2)

    existing_products = [existing_product]

    product_data = {"name": "Мопс", "description": "Умный", "price": 120, "quantity": 3}

    result = Product.new_product(product_data, existing_products)

    assert result is existing_product
    assert isinstance(result, Product)
    assert result.quantity == 5
    assert result.price == 120


def test_new_product_duplicate_old_price_higher():
    existing_product = Product("Мопс", "Красивый", 150, 2)

    existing_products = [existing_product]

    product_data = {"name": "Мопс", "description": "Умный", "price": 100, "quantity": 3}

    result = Product.new_product(product_data, existing_products)

    assert result is existing_product
    assert result.quantity == 5
    assert result.price == 150


def test_price_setter_positive():
    product = Product("Мопс", "Красивый", 100, 2)

    product.price = 200

    assert product.price == 200


def test_price_setter_zero(capsys):
    product = Product("Мопс", "Красивый", 100, 2)

    product.price = 0

    captured = capsys.readouterr()

    assert captured.out == "Цена не должна быть нулевая или отрицательная\n"
    assert product.price == 100


def test_price_setter_negative(capsys):
    product = Product("Мопс", "Красивый", 100, 2)

    product.price = -50

    captured = capsys.readouterr()

    assert captured.out == "Цена не должна быть нулевая или отрицательная\n"
    assert product.price == 100


def test_price_decrease_confirmed(monkeypatch):
    product = Product("Мопс", "Красивый", 200, 2)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    product.price = 100

    assert product.price == 100


def test_price_decrease_rejected(monkeypatch):
    product = Product("Мопс", "Красивый", 200, 2)

    monkeypatch.setattr("builtins.input", lambda _: "n")

    product.price = 100

    assert product.price == 200


def test_price_decrease_invalid_answer(monkeypatch):
    product = Product("Мопс", "Красивый", 200, 2)

    monkeypatch.setattr("builtins.input", lambda _: "abc")

    product.price = 100

    assert product.price == 200


def test_iterator_iter():
    product1 = Product("Телефон", "Описание", 1000, 4)
    category = Category("Электроника", "Техника", [product1])

    iterator = Iterator(category)

    assert iter(iterator) is iterator


def test_iterator():
    product1 = Product("Телефон", "Описание", 1000, 4)
    product2 = Product("Ноутбук", "Описание", 10000, 5)

    category = Category("Электроника", "Техника", [product1, product2])

    iterator = Iterator(category)

    assert next(iterator) == product1
    assert next(iterator) == product2

    with pytest.raises(StopIteration):
        next(iterator)


def test_iterator_for():
    product1 = Product("Телефон", "Описание", 1000, 2)
    product2 = Product("Ноутбук", "Описание", 2000, 3)

    category = Category("Электроника", "Техника", [product1, product2])

    iterator = Iterator(category)

    result = list(iterator)

    assert result == [product1, product2]


def test_get_products_for_iterator():
    product1 = Product("Телефон", "Описание", 1000, 4)
    product2 = Product("Ноутбук", "Описание", 10000, 5)

    category = Category("Электроника", "Техника", [product1, product2])

    assert category.get_products_for_Iterator() == [product1, product2]


def test_smartphone_init(smartphone):
    assert smartphone.efficiency == 2
    assert smartphone.model == "Samsung S 25"
    assert smartphone.memory == 8
    assert smartphone.color == "red"
    assert smartphone.name == "Смартфон"
    assert smartphone.price == 120999.99
    assert smartphone.quantity == 16
    assert smartphone.description == "Хороший выбор"


def test_lawn_grass_init(lawn_grass):
    assert lawn_grass.name == "Газон"
    assert lawn_grass.description == "Хороший газон"
    assert lawn_grass.price == 500
    assert lawn_grass.quantity == 10
    assert lawn_grass.country == "Россия"
    assert lawn_grass.germination_period == "10 дней"
    assert lawn_grass.color == "Зеленый"


def test_smartphone_addition(smartphone):
    smartphone_2 = Smartphone(
        "Смартфон 2",
        "Другой смартфон",
        100000,
        5,
        3,
        "iPhone",
        12,
        "black",
    )

    assert smartphone + smartphone_2 == (
        smartphone.price * smartphone.quantity
        + smartphone_2.price * smartphone_2.quantity
    )


def test_lawn_grass_addition(lawn_grass):
    lawn_grass_2 = LawnGrass(
        "Газон 2",
        "Другой газон",
        300,
        20,
        "Германия",
        "7 дней",
        "Темно-зеленый",
    )

    assert lawn_grass + lawn_grass_2 == (
        lawn_grass.price * lawn_grass.quantity
        + lawn_grass_2.price * lawn_grass_2.quantity
    )


def test_different_products_addition_raises_type_error(
    smartphone,
    lawn_grass,
):
    with pytest.raises(TypeError):
        smartphone + lawn_grass


def test_category_add_product_accepts_smartphone(smartphone):
    category = Category("Телефоны", "Смартфоны", [])

    category.add_product(smartphone)

    assert smartphone in category.get_products_for_Iterator()


def test_category_add_product_accepts_lawn_grass(lawn_grass):
    category = Category("Газон", "Трава", [])

    category.add_product(lawn_grass)

    assert lawn_grass in category.get_products_for_Iterator()


def test_category_add_product_rejects_invalid_object():
    category = Category("Телефоны", "Смартфоны", [])

    with pytest.raises(TypeError):
        category.add_product("не продукт")
