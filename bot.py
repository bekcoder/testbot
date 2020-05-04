import telebot
import pyowm
import pyowm.exceptions
import time as tm
from telebot import types
from pyowm.exceptions import api_response_error
from config import BOT_TOKEN, OWM_TOKEN
from utils.weather import get_forecast
from utils.world_time import get_time
from utils.news import get_article
from utils.stocks import *
from utils.crypto_coins import *
from utils.translate import *
from googletrans import Translator

bot = telebot.TeleBot('1122690762: Aagjrrxyuymu8pbtoxtgjljvgmzpde8l72i', threaded=False)
owm = pyowm.OWM('1122690762:AAGJrRxyUYMU8pbToxtgJlJVGMZpde8l72I', language='uz')
trans = Translator()


@bot.message_handler(commands=['start'])
def command_start(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time','/translate',)
	bot.send_message(message.chat.id, "🤖 Bot ishga tushurildi!\n⚙  /help komandasi orqali bot haqida bilib oling")
	bot.send_message(message.from_user.id, "⌨️ Tugmalar qoshildi!\n⌨️ Tugmalarni yashirish uchun /hide", reply_markup=start_markup)


@bot.message_handler(commands=['hide'])
def command_hide(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.chat.id, "⌨💤...", reply_markup=hide_markup)


@bot.message_handler(commands=['help'])
def command_help(message):
	bot.send_message(message.chat.id, "🤖 /start - tugmalarni qaytarish\n"
									  "☁ /weather - ob-havo\n"
									  "⌛️ /world_time - dunyo soatlari\n"
									  "🔁 /translate - tarjimon")


@bot.message_handler(commands=['weather'])
def command_weather(message):
	sent = bot.send_message(message.chat.id, "🗺 Davlat yoki shahar nomini kiriting\n🔍 Masalan:  Namangan  yoki  Uzbekistan")
	bot.register_next_step_handler(sent, send_forecast)


def send_forecast(message):
	try:
		get_forecast(message.text)
	except pyowm.exceptions.api_response_error.NotFoundError:
		bot.send_message(message.chat.id, "❌  Notog'ri joy, Xatongizni tekshirib keyin yuboring")
	forecast = get_forecast(message.text)
	bot.send_message(message.chat.id, forecast)


@bot.message_handler(commands=['world_time'])
def command_world_time(message):
	sent = bot.send_message(message.chat.id, "🗺 Davlat yoki shahar nomini kiriting\n🔍 Masalan:  Namangan  yoki  Uzbekistan")
	bot.register_next_step_handler(sent, send_time)


def send_time(message):
	try:
		get_time(message.text)
	except IndexError:
		bot.send_message(message.chat.id, "❌  Notog'ri joy, Xatongizni tekshirib keyin yuboring")
	time = get_time(message.text)
	bot.send_message(message.chat.id, time)


@bot.message_handler(commands=['translate'])
def command_translate(message):
	trans_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	trans_markup.row('German', 'French', 'Spanish')
	trans_markup.row('Russian', 'Japanese', 'English')
	sent = bot.send_message(message.chat.id, "📃 Qaysi tilga tarjima qilasiz?", reply_markup=trans_markup)
	bot.register_next_step_handler(sent, get_input)


def get_input(message):
	if not any(message.text in item for item in languages):
		hide_markup = telebot.types.ReplyKeyboardRemove()
		bot.send_message(message.chat.id, "❌ Notog'ri til tugmalardan foydalangan holda tanlang...", reply_markup=hide_markup) 
	else:
		sent = bot.send_message(message.chat.id, "🚩 Uzbek tiligan " + message.text + "\n➡️tarjima qilmoqchi bolgan sozingiz...")
		languages_switcher = {
			'Russian': send_rus_trans,
			'German': send_ger_trans,
			'Japanese': send_jap_trans,
			'English': send_pol_trans,
			'Spanish': send_spa_trans,
			'French': send_fra_trans
		}
	
		lang_response = languages_switcher.get(message.text)
		bot.register_next_step_handler(sent, lang_response)


def send_rus_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False) #Return to start keyboard
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time','/translate',)
	bot.send_message(message.chat.id, to_ru(message.text), reply_markup=start_markup)


def send_ger_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time','/translate',)
	bot.send_message(message.chat.id, to_de(message.text), reply_markup=start_markup)


def send_jap_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time','/translate',)
	bot.send_message(message.chat.id, to_ja(message.text), reply_markup=start_markup)


def send_pol_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time','/translate',)
	bot.send_message(message.chat.id, to_pl(message.text), reply_markup=start_markup)


def send_spa_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time','/translate',)
	bot.send_message(message.chat.id, to_es(message.text), reply_markup=start_markup)

	
def send_fra_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time','/translate',)
	bot.send_message(message.chat.id, to_fr(message.text), reply_markup=start_markup)

	
while True:
	try:
		bot.infinity_polling(True)
	except Exception:
		tm.sleep(1)
