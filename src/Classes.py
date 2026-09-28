class Product:
    """Класс представления продукта"""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт"

    def __add__(self, other):
        if type(other) is type(self):
            return self.__price * self.quantity + other.price * other.quantity
        else:
            raise TypeError

    @classmethod
    def new_product(cls, product_data: dict, existing_products):
        for prod in existing_products:
            if prod.name == product_data["name"]:
                prod.quantity += product_data["quantity"]
                prod.price = max(prod.price, product_data["price"])
                return prod
        return cls(
            product_data["name"],
            product_data["description"],
            product_data["price"],
            product_data["quantity"],
        )

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        if price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif price < self.__price:
            answer = input("Предложенная цена ниже действующей, обновить?")
            if answer.lower() == "y":
                self.__price = price
        else:
            self.__price = price


class Category:
    """Класс подсчета категорий"""

    name: str
    description: str
    products: list

    product_count = 0
    category_count = 0

    def __init__(self, name: str, description: str, products: list[Product]):
        self.name = name
        self.description = description
        self.__products = products
        Category.product_count += len(products)
        Category.category_count += 1

    def __str__(self):
        quantity_prod = 0
        for prod in self.__products:
            quantity_prod += prod.quantity
        return f"{self.name}, количество продуктов: {quantity_prod} шт."

    def get_products_for_Iterator(self):
        return self.__products

    @property
    def products(self):
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

    def add_product(self, product):
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Неверный объект добавления")


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Iterator:
    """Вспомогательный класс, с помощью которого можно перебирать товары одной категории"""

    def __init__(self, category):
        self.obj_Category = category
        self.data = self.obj_Category.get_products_for_Iterator()
        self.current_index = 0

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.data):
            product = self.data[self.current_index]
            self.current_index += 1
            return product
        else:
            raise StopIteration
