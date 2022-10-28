import random

import googletrans
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from googletrans import Translator

token = '5639183049:AAGoBeVx8LHxqMMRWMIVPkFQuv5fGIbQSo8'
bot = Bot(token=token)
dp = Dispatcher(bot)
correct = ''


@dp.message_handler(commands=['start'])
async def Start(message: types.Message):
    await message.answer('привет, я бот переводчик.')
    await message.answer(message.from_user.first_name)
    await message.answer_photo('https://vjoy.cc/wp-content/uploads/2020/10/dlya_dushi_35_13130628.jpg')
    await message.answer_photo(open('kossmoss.png', 'rb'))


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    try:
        text = message.get_args()
        await message.answer(text)
    except:
        return


@dp.message_handler(commands=['translate'])
async def trans(message: types.Message):
    print(googletrans.LANGCODES)
    try:
        translator = Translator()
        text = message.get_args()
        text = text.split(' ! ')
        print(text)
        perevod = translator.translate(text[0], src=text[1], dest=text[2])
        print(perevod)
        await message.answer(perevod.text)
    except:
        await message.answer('Язык не найден.')


@dp.message_handler(commands=['game'])
async def Game(message: types.Message):
    global correct
    trans = Translator()
    with open('sda.txt', 'r', encoding='utf-8') as file:
        a = file.readline().split()
    weriant = []
    correct = random.choice(a)
    correcten = trans.translate(correct, src='ru', dest='en')
    i = 1

    while i != 5:
        w = random.choice(a)
        if trans.translate(w, src='ru', dest='en') not in weriant:
            weriant.append(trans.translate(w, src='ru', dest='en'))
            i += 1
    weriant.insert(random.randint(0, 5), correcten)

    bottoms = types.InlineKeyboardMarkup()

    for i in range(5):
        print('!!')
        if weriant[i].text != correcten.text:
            b1 = types.InlineKeyboardButton(text=weriant[i].text, callback_data=correcten.text)
            bottoms.add(b1)
            print('1')
        else:
            b1 = types.InlineKeyboardButton(text=correcten.text, callback_data='1')
            bottoms.add(b1)
            print('2')

    await bot.send_message(message.chat.id, 'выберете перевод этого слова ' + correct, reply_markup=bottoms)


@dp.callback_query_handler(lambda call: True)
async def tamoj(call):
    await call.message.delete()
    if call.data == '1':
        await bot.send_message(call.message.chat.id, 'правильно!')

    else:
        await bot.send_message(call.message.chat.id, 'неправильно, правильный ответ: ' + call.data)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
