import logging
from aiogram import Bot,types,executor,Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup , KeyboardButton
from db import Database

logging.basicConfig(level=logging.INFO)

class Buyurtma(StatesGroup):
    id = State()
    ism = State()
    viloyat = State()
    tuman = State()
    mahalla = State()
    kontakt = State()
    lokatsiya = State()


bot = Bot(token="5608037183:AAEstsFk4YEn3eXn7dP3mD4sBt8XQpCOCxY")
dp= Dispatcher(bot , storage = MemoryStorage())
db = Database("database.db")

@dp.message_handler(commands='start', state=None)
async def start(mess:types.Message):
    await mess.answer('Salom botga xush kelibsiz\nHurmatli mijoz siz qanday ID li mahsulotimizni buyurtma qilmoqchisiz?')
    await Buyurtma.id.set()

@dp.message_handler(state = Buyurtma.id)
async def id(mess:types.Message,state:FSMContext):
    await state.update_data({"id":mess.text})
    await mess.answer("Iltimos ism va familiyangizni kiriting")
    await Buyurtma.next()

@dp.message_handler(state=Buyurtma.ism)
async def ism(mess:types.Message,state:FSMContext):
    await state.update_data({"ism":mess.text})
    await mess.answer("Viloyatingiz kiriting")
    await Buyurtma.next()

@dp.message_handler(state=Buyurtma.viloyat)
async def viloyat(mess:types.Message,state:FSMContext):
    await state.update_data({"viloyat":mess.text})
    await mess.answer("Tumaningizni kiriting")
    await Buyurtma.next()

@dp.message_handler(state= Buyurtma.tuman)
async def tuman(mess:types.Message,state:FSMContext):
    await state.update_data({"tuman":mess.text})
    await mess.answer("Mahalla va uy raqamingizni to'liq kiriting")
    await Buyurtma.next()

@dp.message_handler(state=Buyurtma.mahalla)
async def mahalla(mess:types.Message,state:FSMContext):
    await state.update_data({"mahalla":mess.text})
    contactmp = ReplyKeyboardMarkup(resize_keyboard= True,one_time_keyboard=True)
    contact = KeyboardButton(text="Kontakt ulashish",request_contact = True)
    contactmp.add(contact)
    await mess.answer("Telefon raqamingizni kiriting",reply_markup=contactmp)
    await Buyurtma.next()

@dp.message_handler(state=Buyurtma.kontakt,content_types="contact")
async def kontakt(mess:types.Message,state:FSMContext):
    await state.update_data({"kontakt":mess.contact.phone_number})
    locationmp= ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    location= KeyboardButton(text="Joylashuv ulashish",request_location=True)
    locationmp.add(location)
    await mess.answer("Iltimos ma'lumotlarini kiritgan uyingizni lokatsiyasini yuboring\nBu bizga va sizga mahsulotimiz o'z vaqtida yetib borishi uchun\nKatta ahamiyatga ega",reply_markup=locationmp)
    await Buyurtma.next()


@dp.message_handler(state=Buyurtma.lokatsiya,content_types="location")
async def lokatsiya(mess:types.Message, state:FSMContext):
    await state.update_data({"lokatsiya":mess.location.longitude})
    data = await state.get_data()
    db.add_buyurtma(id = data['id'],ism=data['ism'],viloyat= data['viloyat'],tuman=data['tuman'],mahalla=data['mahalla'],raqam=data['kontakt'],joylashuv=data['lokatsiya'])
    await bot.send_message(1812487581,f"Mahsulot id:{data['id']}\nMijoz ism familiyasi:{data['ism']}\nViloyat:{data['viloyat']}\nTuman:{data['tuman']}\nMahalla:{data['mahalla']}\nTelefon raqam:{data['kontakt']}")
    await mess.answer("Hurmatli mijoz sizning ma'lumotlaringiz bizning\nMa'lumotlar bazamizga kelib tushdi\nBiz mahsulotimizni siz kiritgan manzilga albatta\nBelgilangan vaqtda yetkazib boramiz ishonchingiz\nuchun raxmat aytib qolamiz hurmatli mijoz!!!")
    await state.finish()



if __name__=="__main__":
    executor.start_polling(dp,skip_updates=True)