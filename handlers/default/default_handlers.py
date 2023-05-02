from aiogram import types
from aiogram.dispatcher import FSMContext

from Cakeshop_Euphoria_Bot.main import dp, bot
from Cakeshop_Euphoria_Bot import keyboards

HELP_MESSAGE = """
*Список доступных команд:*

*/start* - _Начать работу с ботом_
*/help* - _Список команд_
*/info* - _Вывод информации о боте_
"""


@dp.message_handler(commands=['start'])
async def start_func(message: types.Message):
    await message.answer(
        text=f'Добро пожаловать в кондитерскую, *{message.from_user.first_name}*!\nВыбери свою роль:',
        reply_markup=keyboards.inline.ikb.get_start_ikb(), parse_mode='Markdown')


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=HELP_MESSAGE, parse_mode='Markdown')
    await message.delete()


@dp.message_handler(commands=['info'])
async def start_func(message: types.Message):
    await message.answer(text='Данный бот создан для взаимодействия с кондитерской *Euphoria*.',
                         parse_mode='Markdown')


@dp.callback_query_handler(text='main_menu')
async def go_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.answer("Выбери свою роль:",
                                  reply_markup=keyboards.inline.ikb.get_start_ikb())
    await callback.answer()
