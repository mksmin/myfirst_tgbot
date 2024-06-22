# Импортируем библиотеки
import os
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
import qrcode

router = Router() # Выполняет роль диспетчера

# Хэндлер на команду /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!\nВроде все работает, как надо. Чтобы получить QR - просто пришли ссылку')

async def get_qr(link_qr, user_id): # Генерируем QR код в директории, которую указали в .env
    qr_path_imp = os.getenv('QR_PATH')
    img = qrcode.make(link_qr)
    qr_path = f'{qr_path_imp}qr_user_{user_id}.png'
    img.save(qr_path)
    return qr_path
    
async def remove_qr(qr_path): # удаляет сгенерированный QR с сервера (пока что незачем его хранить)
    os.remove(os.path.join(qr_path))

async def start_mess(message):
    print(message)
    await message.answer(f'Привет, {message.from_user.first_name}, \nТвое сообщение - {message.text}')

start = ['Привет', 'Здарова', 'привет', 'здарова']

# После этого комментария пишу хэндлеры. Все, что до - фукнции, кроме /start

@router.message()
async def text_entitles(message: Message):
    entitles = message.entities
    match entitles:
        case None:
            count = 0
            for i in start:
                if i in message.text and count == 0:
                    count += 1
                    await start_mess(message)
                    break
        case _:
            for item in entitles:
                if item.type == 'url':
                    link = item.extract_from(message.text)
                    user_id = message.from_user.id
                    qr_path_mes = await get_qr(link, user_id)
                    await message.reply_photo(photo=FSInputFile(path=qr_path_mes),
                                              filename="qrcodelink.png",
                                              caption=f'QR на {link}')
                    await remove_qr(qr_path_mes)
