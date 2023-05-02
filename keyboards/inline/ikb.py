from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

products_correct_cb = CallbackData("product", "id", "action")


def get_start_ikb() -> InlineKeyboardMarkup:
    """Создание начальной клавиатуры"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Администратор',
                              callback_data='admin')],
        [InlineKeyboardButton('Клиент',
                              callback_data='client')],
    ])

    return ikb


def get_start_registration_ikb() -> InlineKeyboardMarkup:
    """Создание клавиатуры регистрации клиента"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Начать регистрацию',
                              callback_data='registration')],
    ])

    return ikb


def get_showing_production_ikb() -> InlineKeyboardMarkup:
    """Создание клавиатуры просмотра продукции клиента"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Просмотреть продукцию',
                              callback_data='show_production')],
        [InlineKeyboardButton('Переход в главное меню',
                              callback_data='main_menu')],
    ])

    return ikb


def get_choice_production_ikb(product_id: int) -> InlineKeyboardMarkup:
    """Создание клавиатуры выбора продукции клиента"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Выбрать продукцию',
                              callback_data=products_correct_cb.new(id=product_id,
                                                                    action='choice_production'))]
    ])

    return ikb


def get_choice_production_ikb_with_main_menu(product_id: int) -> InlineKeyboardMarkup:
    """Создание клавиатуры выбора продукции клиента"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Выбрать продукцию',
                              callback_data=products_correct_cb.new(id=product_id,
                                                                    action='choice_production'))],
        [InlineKeyboardButton('Переход в главное меню',
                              callback_data='main_menu')]
    ])

    return ikb


def get_admin_menu_ikb() -> InlineKeyboardMarkup:
    """Создание клавиатуры меню админа"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Просмотр списка постоянных клиентов',
                              callback_data='client_list')],
        [InlineKeyboardButton('Просмотр списка заказов',
                              callback_data='order_list')],
        [InlineKeyboardButton('Статистика за день',
                              callback_data='statistics')],
        [InlineKeyboardButton('Добавление новой продукции в кондитерскую',
                              callback_data='add_products')],
        [InlineKeyboardButton('Просмотр и редактирование продукции в кондитерской',
                              callback_data='show_products')],
        [InlineKeyboardButton('Переход в главное меню',
                              callback_data='main_menu')],
    ])

    return ikb


def go_to_main_menu_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Переход в главное меню',
                              callback_data='main_menu')],
    ])
    return ikb


def get_delete_update_ikb(product_id: int) -> InlineKeyboardMarkup:
    """Клавиатура редактирования и удаления продукта"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Редактировать данные о продукте',
                              callback_data=products_correct_cb.new(id=product_id,
                                                                    action='update_product'))],
        [InlineKeyboardButton('Удалить продукт',
                              callback_data=products_correct_cb.new(id=product_id,
                                                                    action='delete_product'))]
    ])

    return ikb


def get_edit_product_ikb(product_id: int) -> InlineKeyboardMarkup:
    """Клавиатура редактирования продукта"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Продолжить редактировать данные о продукте',
                              callback_data=products_correct_cb.new(id=product_id,
                                                                    action='continue_update'))],
        [InlineKeyboardButton('Завершить редактирование данных',
                              callback_data=products_correct_cb.new(id=product_id,
                                                                    action='stop_update'))]
    ])

    return ikb
