from aiogram.dispatcher.filters.state import StatesGroup, State

class ProductState(StatesGroup):
    """Класс состояний создания продукта"""
    title = State()
    ingredients = State()
    photo = State()
    price = State()
    quantity = State()
    confirm = State()

    # Состояния изменения продукта
    edit_title = State()
    edit_ingredients = State()
    edit_photo = State()
    edit_price = State()
    edit_quantity = State()
    edit_confirm = State()


class ClientState(StatesGroup):
    """Класс состояний регистрации клиента"""
    name = State()
    surname = State()
    phone = State()
    email = State()


class OrderState(StatesGroup):
    """Класс состояний заказа продукции клиентом"""
    title = State()
    quantity = State()
    address = State()
    time = State()
    phone_recepient = State()