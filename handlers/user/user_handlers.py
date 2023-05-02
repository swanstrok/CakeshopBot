from Cakeshop_Euphoria_Bot.keyboards import *
from Cakeshop_Euphoria_Bot.main import dp, bot, db
from aiogram import types
from Cakeshop_Euphoria_Bot.filters import IsUser
from aiogram.dispatcher import FSMContext
from Cakeshop_Euphoria_Bot.states import states
import time

pr = db.fetchall("SELECT client_id FROM clients")
data_clients = [int(*i) for i in pr]


@dp.callback_query_handler(IsUser(), text='client')
async def base_client(callback: types.CallbackQuery):
    """Функция выводит меню клиента"""
    if callback.from_user.id in data_clients:
        await callback.message.answer(f"Здравствуйте, *{callback.from_user.first_name}*!",
                                      parse_mode='Markdown',
                                      reply_markup=inline.ikb.get_showing_production_ikb())
        await callback.message.delete()
    else:
        await callback.message.answer(
            "Вас нет в списке наших клиентов, пожалуйста пройдите регистрацию.",
            reply_markup=inline.ikb.get_start_registration_ikb())
    await callback.answer()


@dp.callback_query_handler(IsUser(), text='registration')
async def registration_process(callback: types.CallbackQuery):
    """Отправка запроса на регистрацию нового клиента"""
    await callback.message.answer("Введите ваше имя:")
    await states.ClientState.name.set()


@dp.message_handler(IsUser(), state=states.ClientState.name)
async def load_name(message: types.Message, state: FSMContext):
    """Загрузка имени нового клиента"""
    await state.update_data(name=message.text.capitalize())
    await message.answer('Введите вашу фамилию:')
    await states.ClientState.next()


@dp.message_handler(IsUser(), state=states.ClientState.surname)
async def load_surname(message: types.Message, state: FSMContext):
    """Загрузка фамилии нового клиента"""
    await state.update_data(surname=message.text.capitalize())
    await message.answer('Введите ваш телефон:')
    await states.ClientState.next()


@dp.message_handler(IsUser(), state=states.ClientState.phone)
async def load_phone(message: types.Message, state: FSMContext):
    """Загрузка номера телефона нового клиента"""
    await state.update_data(phone=message.text)
    await message.answer('Введите ваш email:')
    await states.ClientState.next()


@dp.message_handler(IsUser(), state=states.ClientState.email)
async def load_email(message: types.Message, state: FSMContext):
    """Загрузка email и ID нового клиента"""
    await state.update_data(email=message.text)
    await state.update_data(client_id=message.from_user.id)
    data = await state.get_data()
    await state.finish()

    db.query(
        "INSERT INTO clients (name, surname, phone, email, client_id) VALUES (?, ?, ?, ?, ?)",
        (data['name'], data['surname'], data['phone'], data['email'], data['client_id']))
    await bot.send_message(chat_id=message.from_user.id, text="Спасибо за вашу регистрацию.")
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Имя:{data['name']}\n"
                                f"Фамилия: {data['surname']}\n"
                                f"Телефон: {data['phone']}\n"
                                f"Email: {data['email']}",
                           reply_markup=inline.ikb.get_showing_production_ikb())


async def show_all_products(callback: types.CallbackQuery, products: list):
    """Функция вывода на экран продукции"""
    for index, item in enumerate(products):
        if index != len(products) - 1:
            await bot.send_photo(chat_id=callback.message.chat.id, photo=item[3],
                                 caption=f"*{item[1]}*\n"
                                         f"Состав: {item[2]}\n"
                                         f"Цена: {item[4]} руб.\n"
                                         f"Остаток: {item[5]}\n",
                                 parse_mode='Markdown',
                                 reply_markup=inline.ikb.get_choice_production_ikb(item[0]))
        else:
            await bot.send_photo(chat_id=callback.message.chat.id, photo=item[3],
                                 caption=f"*{item[1]}*\n"
                                         f"Состав: {item[2]}\n"
                                         f"Цена: {item[4]} руб.\n"
                                         f"Остаток: {item[5]}\n",
                                 parse_mode='Markdown',
                                 reply_markup=inline.ikb.get_choice_production_ikb_with_main_menu(
                                     item[0]))

    await callback.answer()
    await callback.message.delete()


async def input_quantity(message: types.Message):
    await message.answer('Введите желаемое количество товара:')


@dp.callback_query_handler(IsUser(),
                           inline.ikb.products_correct_cb.filter(action='choice_production'))
async def order_registration_process(callback: types.CallbackQuery, callback_data: dict,
                                     state: FSMContext):
    """Отправка запроса на создание нового заказа"""
    await states.OrderState.title.set()
    title = db.fetchone("SELECT title FROM production WHERE id = ?", (callback_data['id'],))[0]
    await state.update_data(title=title)
    await input_quantity(callback.message)
    await states.OrderState.next()


@dp.message_handler(IsUser(), state=states.OrderState.quantity)
async def order_load_quantity(message: types.Message, state: FSMContext):
    """Загрузка количества продукции в заказе"""
    quantity_desired = int(message.text)
    data = await state.get_data()
    title = data['title']
    quantity_real = db.fetchone('SELECT quantity FROM production WHERE title = ?', (title,))
    if int(quantity_desired) > int(*quantity_real):
        await message.reply("Простите у нас нет столько в наличии, закажите иное количество.")
        await states.OrderState.quantity.set()
        await input_quantity(message)
    else:
        await state.update_data(quantity=int(message.text))
        price = db.fetchone('SELECT price FROM production WHERE title = ?', (title,))
        cost = int(*price) * int(message.text)
        await state.update_data(cost=cost)
        await message.answer('Введите адрес доставки:')
        await states.OrderState.next()


@dp.message_handler(IsUser(), state=states.OrderState.address)
async def order_load_address(message: types.Message, state: FSMContext):
    """Загрузка адреса доставки в заказе"""
    await state.update_data(address=message.text)
    await message.answer('Введите желаемую дату и время для доставки (DD.MM.YYYY/HH:MI)')
    await states.OrderState.next()


@dp.message_handler(IsUser(), state=states.OrderState.time)
async def order_load_time(message: types.Message, state: FSMContext):
    """Загрузка времени доставки в заказе"""
    await state.update_data(time_delivery=message.text)

    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    await state.update_data(time_order=current_time)
    await message.answer('Введите телефон получателя:')
    await states.OrderState.next()


@dp.message_handler(IsUser(), state=states.OrderState.phone_recepient)
async def order_load_phone_recepient(message: types.Message, state: FSMContext):
    """Загрузка телефона получателя в заказе"""
    await state.update_data(phone_recepient=message.text)
    phone_sender = \
        db.fetchone("SELECT phone FROM clients WHERE client_id = ?", (message.from_user.id,))[0]

    await state.update_data(phone_sender=phone_sender)
    await state.update_data(delivered=False)
    await message.answer('Ваш заказ оформлен.')

    data = await state.get_data()
    await state.finish()

    db.query(
        "INSERT INTO orders (title, quantity, address, time_order, time_delivery, phone_sender,\
         phone_recepient, cost, delivered) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            data['title'], data['quantity'], data['address'], data['time_order'],
            data['time_delivery'], data['phone_sender'], data['phone_recepient'], data['cost'],
            data['delivered']))

    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Название товара: {data['title']}\n"
                                f"Количество: {data['quantity']}\n"
                                f"Адрес доставки: {data['address']}\n"
                                f"Дата и время доставки: {data['time_delivery']}\n"
                                f"Телефон заказчика: {data['phone_sender']}\n"
                                f"Телефон получателя: {data['phone_recepient']}\n"
                                f"Время заказа: {data['time_order']}\n"
                                f"*Сумма к оплате: {data['cost']} руб.*",
                           parse_mode='Markdown',
                           reply_markup=inline.ikb.get_showing_production_ikb())

    # Выведение остатков продукции
    quantity_real = db.fetchone('SELECT quantity FROM production WHERE title = ?', (data['title'],))
    quantity_ordered = data['quantity']
    remainder = int(*quantity_real) - int(quantity_ordered)

    db.query("UPDATE production SET quantity = ? WHERE title = ?", (remainder, data['title']))


@dp.callback_query_handler(IsUser(), text='show_production')
async def show_production(callback: types.CallbackQuery) -> None:
    """Функция отображения продукции"""
    products = db.fetchall("SELECT * FROM production WHERE confirm = TRUE AND quantity > 0")
    if not products:
        return await callback.answer(
            "На данный момент вся наша продукция закончилась. Приносим свои извинения!",
            show_alert=True)

    await show_all_products(callback=callback, products=products)
