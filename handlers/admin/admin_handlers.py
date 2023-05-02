from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from Cakeshop_Euphoria_Bot.main import dp, bot, db
from Cakeshop_Euphoria_Bot.filters import IsAdmin
from aiogram import types
from Cakeshop_Euphoria_Bot.keyboards import *
from Cakeshop_Euphoria_Bot.config import ADMINS
from Cakeshop_Euphoria_Bot.states import states


@dp.callback_query_handler(text='admin')
async def admin_menu(callback: types.CallbackQuery):
    """Функция выводит меню админа"""
    if callback.from_user.id in ADMINS:
        await callback.message.answer('Выберите опцию:',
                                      reply_markup=inline.ikb.get_admin_menu_ikb())
        await callback.answer()
    else:
        await callback.answer(text="Я тебя не знаю, ты не мой админушка! 😡", show_alert=True)


@dp.callback_query_handler(IsAdmin(), text='client_list')
async def show_client_list(callback: types.CallbackQuery) -> None:
    data = db.fetchall("SELECT * FROM clients")
    print(data)
    for index, client in enumerate(data):
        if index != len(data) - 1:
            await callback.message.answer(f"Имя: {client[1]}\n"
                                          f"Фамилия: {client[2]}\n"
                                          f"Телефон: {client[3]}\n"
                                          f"email: {client[4]}\n"
                                          f"client_id: {client[5]}")
        else:
            await callback.message.answer(f"Имя: {client[1]}\n"
                                          f"Фамилия: {client[2]}\n"
                                          f"Телефон: {client[3]}\n"
                                          f"email: {client[4]}\n"
                                          f"client_id: {client[5]}",
                                          reply_markup=inline.ikb.go_to_main_menu_ikb())
    await callback.answer()





@dp.callback_query_handler(IsAdmin(), text='order_list')
async def show_order_list(callback: types.CallbackQuery) -> None:
    data = db.fetchall("SELECT * FROM orders")
    print(data)
    for index, client in enumerate(data):

        if client[9] == 0:
            status = "Не доставлен"
        else:
            status = "Доставлен"

        if index != len(data) - 1:
            await callback.message.answer(f"*{client[1]}*\n"
                                          f"Количество: {client[2]}\n"
                                          f"Адрес доставки: {client[3]}\n"
                                          f"Время заказа: {client[4]}\n"
                                          f"Время доставки: {client[5]}\n"
                                          f"Телефон заказчика: {client[6]}\n"
                                          f"Телефон получателя: {client[7]}\n"
                                          f"Сумма заказа: {client[8]} руб.\n"
                                          f"Статус заказа: *{status}*",
                                          parse_mode='Markdown')
        else:
            await callback.message.answer(f"*{client[1]}*\n"
                                          f"Количество: {client[2]}\n"
                                          f"Адрес доставки: {client[3]}\n"
                                          f"Время заказа: {client[4]}\n"
                                          f"Время доставки: {client[5]}\n"
                                          f"Телефон заказчика: {client[6]}\n"
                                          f"Телефон получателя: {client[7]}\n"
                                          f"Сумма заказа: {client[8]} руб.\n"
                                          f"Статус заказа: *{status}*",
                                          parse_mode='Markdown',
                                          reply_markup=inline.ikb.go_to_main_menu_ikb())
    await callback.answer()


@dp.message_handler(IsAdmin(), text=['Отмена'], state="*")
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    """Функция отмены создания нового товара"""
    await message.delete()
    await message.answer("Добавление/редактирование продукта отменено.",
                         reply_markup=inline.ikb.get_start_ikb())
    await state.finish()


@dp.callback_query_handler(IsAdmin(), text='add_products')
async def add_product_process(callback: types.CallbackQuery):
    """Отправка запроса на добавление нового товара"""
    await callback.message.answer("Введите название нового продукта",
                                  reply_markup=reply.kb.cancel_add_kb())
    await states.ProductState.title.set()


@dp.message_handler(IsAdmin(), state=states.ProductState.title)
async def load_title(message: types.Message, state: FSMContext):
    """Загрузка названия нового товара"""
    await state.update_data(title=message.text.title())
    await message.answer('Введите состав нового продукта:')
    await states.ProductState.next()


@dp.message_handler(IsAdmin(), state=states.ProductState.ingredients)
async def load_ingredients(message: types.Message, state: FSMContext):
    """Загрузка состава нового товара"""
    await state.update_data(ingredients=message.text.capitalize())
    await message.answer('Отправьте фотографию нового продукта:')
    await states.ProductState.next()


@dp.message_handler(lambda message: not message.photo, state=states.ProductState.photo)
async def check_photo(message: types.Message) -> None:
    """Функция проверки загрузки фотографии нового продукта"""
    await message.answer("Это не фото!", reply_markup=reply.kb.cancel_add_kb())


@dp.message_handler(IsAdmin(), state=states.ProductState.photo, content_types=['photo'])
async def load_photo(message: types.Message, state: FSMContext):
    """Загрузка фотографии нового товара"""
    photo = message.photo[0].file_id
    await state.update_data(photo=photo)
    await message.answer('Введите стоимость нового продукта:')
    await states.ProductState.next()


@dp.message_handler(IsAdmin(), state=states.ProductState.price)
async def load_price(message: types.Message, state: FSMContext):
    """Загрузка цены нового товара"""
    await state.update_data(price=int(message.text))
    await message.answer('Отправьте количество нового продукта:')
    await states.ProductState.next()


@dp.message_handler(IsAdmin(), state=states.ProductState.quantity)
async def load_quantity(message: types.Message, state: FSMContext):
    """Загрузка количества нового товара"""
    await state.update_data(quantity=int(message.text))
    await message.answer('Вы действительно хотите отображать новый товар в продукции (да/нет):')
    await states.ProductState.next()


@dp.message_handler(IsAdmin(), state=states.ProductState.confirm)
async def load_cofirm(message: types.Message, state: FSMContext):
    """Подтверждение создания нового товара"""
    if message.text.lower() == 'да':
        await state.update_data(confirm=True)
    elif message.text.lower() == 'нет':
        await state.update_data(confirm=False)

    data = await state.get_data()
    await state.finish()

    db.query(
        "INSERT INTO production (title, ingredients, photo, price, quantity, confirm) VALUES (?, ?, ?, ?, ?, ?)",
        (data['title'], data['ingredients'], data['photo'], data['price'], data['quantity'],
         data['confirm']))

    await message.answer("Данные о новом продукте успешно загружены.",
                         reply_markup=ReplyKeyboardRemove())
    await bot.send_photo(chat_id=message.from_user.id, photo=data['photo'],
                         caption=f"*{data['title']}*\n"
                                 f"Состав: {data['ingredients']}\n"
                                 f"Цена: {data['price']}\n"
                                 f"Остаток: {data['quantity']}\n"
                                 f"Находится в продаже: {'да' if data['confirm'] == 1 else 'нет'}",
                         parse_mode='Markdown',
                         reply_markup=inline.ikb.get_start_ikb())


async def show_all_products(callback: types.CallbackQuery, products: list):
    """Функция вывода на экран продукции"""
    for item in products:
        await bot.send_photo(chat_id=callback.message.chat.id, photo=item[3],
                             caption=f"*{item[1]}*\n"
                                     f"Состав: {item[2]}\n"
                                     f"Цена: {item[4]} руб.\n"
                                     f"Остаток: {item[5]}\n"
                                     f"Находится в продаже: {'да' if item[6] == 1 else 'нет'}",
                             parse_mode='Markdown',
                             reply_markup=inline.ikb.get_delete_update_ikb(item[0]))
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Для выхода в главное меню нажмите кнопку",
                                  reply_markup=inline.ikb.go_to_main_menu_ikb())


@dp.callback_query_handler(IsAdmin(),
                           inline.ikb.products_correct_cb.filter(action='delete_product'))
async def cb_delete_product(callback: types.CallbackQuery, callback_data: dict) -> None:
    """Функция удаления выбранного продукта из продукции"""
    db.query("DELETE FROM production WHERE id = ?", (callback_data['id'],))

    await callback.message.reply('Выбраная вами продукция удалена',
                                 reply_markup=inline.ikb.get_start_ikb())
    await callback.answer()


@dp.callback_query_handler(IsAdmin(), inline.ikb.products_correct_cb.filter(action='stop_update'),
                           state="*")
async def cb_stop_update(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Функция завершения редактирования товара"""
    await callback.message.delete()
    await callback.message.answer("Редактирование продукта завершено.",
                                  reply_markup=inline.ikb.get_start_ikb())
    await state.finish()


@dp.callback_query_handler(IsAdmin(),
                           inline.ikb.products_correct_cb.filter(action='update_product'))
async def cb_update_product_title(callback: types.CallbackQuery, callback_data: dict,
                                  state: FSMContext) -> None:
    """Функция изменения названия выбранного продукта из продукции"""
    await states.ProductState.edit_title.set()
    await callback.message.reply('Отправьте новое название продукта.',
                                 reply_markup=reply.kb.cancel_add_kb())

    await state.update_data(product_id=callback_data['id'])
    await callback.answer()


@dp.message_handler(IsAdmin(), state=states.ProductState.edit_title)
async def load_new_title(message: types.Message, state: FSMContext):
    """Процесс изменения названия продукта"""
    data = await state.get_data()

    db.query("UPDATE production SET title = ? WHERE id = ?",
             (message.text.title(), data['product_id'][0]))

    await message.answer('Новое название продукта установлено.',
                         reply_markup=inline.ikb.get_edit_product_ikb(data['product_id'][0]))


@dp.callback_query_handler(IsAdmin(),
                           inline.ikb.products_correct_cb.filter(action='continue_update'),
                           state=states.ProductState.edit_title)
async def cb_update_product_ingredients(callback: types.CallbackQuery, callback_data: dict,
                                        state: FSMContext) -> None:
    """Функция изменения состава выбранного продукта из продукции"""
    await states.ProductState.edit_ingredients.set()
    await callback.message.answer('Отправьте новый состав продукта.',
                                  reply_markup=reply.kb.cancel_add_kb())

    await state.update_data(product_id=callback_data['id'])
    await callback.answer()


@dp.message_handler(IsAdmin(), state=states.ProductState.edit_ingredients)
async def load_new_ingredients(message: types.Message, state: FSMContext):
    """Процесс изменения состава продукта"""
    data = await state.get_data()

    db.query("UPDATE production SET ingredients = ? WHERE id = ?",
             (message.text.capitalize(), data['product_id'][0]))

    await message.answer('Новый состав продукта установлен.',
                         reply_markup=inline.ikb.get_edit_product_ikb(data['product_id'][0]))


@dp.callback_query_handler(IsAdmin(),
                           inline.ikb.products_correct_cb.filter(action='continue_update'),
                           state=states.ProductState.edit_ingredients)
async def cb_update_product_photo(callback: types.CallbackQuery, callback_data: dict,
                                  state: FSMContext) -> None:
    """Функция изменения фотографии выбранного продукта из продукции"""
    await states.ProductState.edit_photo.set()
    await callback.message.answer('Отправьте новую фотографию продукта:',
                                  reply_markup=reply.kb.cancel_add_kb())

    await state.update_data(product_id=callback_data['id'])
    await callback.answer()


@dp.message_handler(lambda message: not message.photo, state=states.ProductState.edit_photo)
async def check_edit_photo(message: types.Message) -> None:
    """Функция проверки загрузки новой фотографии продукта"""
    await message.answer("Это не фото!", reply_markup=reply.kb.cancel_add_kb())


@dp.message_handler(IsAdmin(), state=states.ProductState.edit_photo, content_types=['photo'])
async def load_edit_photo(message: types.Message, state: FSMContext):
    """Процесс изменения фотографии продукта"""
    data = await state.get_data()

    db.query("UPDATE production SET photo = ? WHERE id = ?",
             (message.photo[0].file_id, data['product_id'][0]))

    await message.answer('Новая фотография продукта установлена.',
                         reply_markup=inline.ikb.get_edit_product_ikb(data['product_id'][0]))


@dp.callback_query_handler(IsAdmin(),
                           inline.ikb.products_correct_cb.filter(action='continue_update'),
                           state=states.ProductState.edit_photo)
async def cb_update_product_price(callback: types.CallbackQuery, callback_data: dict,
                                  state: FSMContext) -> None:
    """Функция изменения цены выбранного продукта из продукции"""
    await states.ProductState.edit_price.set()
    await callback.message.answer('Отправьте новую стоимость продукта.',
                                  reply_markup=reply.kb.cancel_add_kb())

    await state.update_data(product_id=callback_data['id'])
    await callback.answer()


@dp.message_handler(IsAdmin(), state=states.ProductState.edit_price)
async def load_new_price(message: types.Message, state: FSMContext):
    """Процесс изменения цены продукта"""
    data = await state.get_data()

    db.query("UPDATE production SET price = ? WHERE id = ?",
             (int(message.text), data['product_id'][0]))

    await message.answer('Новая цена продукта установлена.',
                         reply_markup=inline.ikb.get_edit_product_ikb(data['product_id'][0]))


@dp.callback_query_handler(IsAdmin(),
                           inline.ikb.products_correct_cb.filter(action='continue_update'),
                           state=states.ProductState.edit_price)
async def cb_update_product_quantity(callback: types.CallbackQuery, callback_data: dict,
                                     state: FSMContext) -> None:
    """Функция изменения количества выбранного продукта в кондитерской"""
    await states.ProductState.edit_quantity.set()
    await callback.message.answer('Отправьте новое количество продукта.',
                                  reply_markup=reply.kb.cancel_add_kb())

    await state.update_data(product_id=callback_data['id'])
    await callback.answer()


@dp.message_handler(IsAdmin(), state=states.ProductState.edit_quantity)
async def load_new_quantity(message: types.Message, state: FSMContext):
    """Процесс изменения количества продукта"""
    data = await state.get_data()

    db.query("UPDATE production SET quantity = ? WHERE id = ?",
             (int(message.text), data['product_id'][0]))

    await message.answer('Количество продукта изменено.',
                         reply_markup=inline.ikb.get_edit_product_ikb(data['product_id'][0]))


@dp.callback_query_handler(IsAdmin(),
                           inline.ikb.products_correct_cb.filter(action='continue_update'),
                           state=states.ProductState.edit_quantity)
async def cb_update_product_confirm(callback: types.CallbackQuery, callback_data: dict,
                                    state: FSMContext) -> None:
    """Функция изменения отображения выбранного продукта в кондитерской"""
    await states.ProductState.edit_confirm.set()
    await callback.message.answer(
        'Вы действительно хотите отображать новый товар в продукции (да/нет):',
        reply_markup=reply.kb.cancel_add_kb())

    await state.update_data(product_id=callback_data['id'])
    await callback.answer()


@dp.message_handler(IsAdmin(), state=states.ProductState.edit_confirm)
async def load_new_confirm(message: types.Message, state: FSMContext):
    """Процесс изменения отображения продукта"""
    data = await state.get_data()
    content = None

    if message.text.lower() == "да":
        content = True
    elif message.text.lower() == 'нет':
        content = False

    db.query("UPDATE production SET confirm = ? WHERE id = ?", (content, data['product_id'][0]))

    await message.answer("Изменение товара завершено", reply_markup=inline.ikb.get_start_ikb())
    await state.finish()


@dp.callback_query_handler(IsAdmin(), text='show_products')
async def show_production(callback: types.CallbackQuery) -> None:
    """Функция отображения продукции"""
    products = db.fetchall('SELECT * FROM production')
    if not products:
        return await callback.answer(
            "На данный момент вся наша продукция закончилась.", show_alert=True)

    await show_all_products(callback=callback, products=products)
