import telebot
import time
from config import TELEGRAM_TOKEN

from logic.ia import ask_ai
from logic.login import register_handlers as register_login
from logic.logout import register_handlers as register_logout
from logic.horarios import format_schedule, get_schedule
from utils.helpers import get_user_by_telegram

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Registrar handlers 
register_login(bot)
register_logout(bot)

# /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Bienvenido al asistente escolar. Usa /login para identificarte.")

#/horario
@bot.message_handler(commands=["horario"])
def horario_handler(message):
    user = get_user_by_telegram(message.from_user.id)

    if not user:
        bot.reply_to(message, "🔒 Necesitas iniciar sesión con /login para ver tu horario.")
        return

    if user[3] != 1:
        bot.reply_to(message, "🔒 Tu sesión no está activa. Usa /login.")
        return

    curso = user[2]
    rows = get_schedule(curso)
    schedule_text = format_schedule(rows)

    bot.reply_to(message, schedule_text, parse_mode="Markdown")
    
# Todos los mensajes pasan por IA si no son comandos ni números(fix error durante login)
@bot.message_handler(func=lambda msg: True)
def main_handler(message):
     
    if message.text.startswith(("/")) or message.text.isdigit():
        return
    
    # Checar si está loggeado
    user = get_user_by_telegram(message.from_user.id)

    if not user:
        bot.reply_to(message, "🔒 Necesitas iniciar sesión con /login para usar el asistente.")
        return

    if user[3] != 1:
        bot.reply_to(message, "🔒 Tu sesión no está activa. Usa /login.")
        return

    # SI ESTÁ LOGGEADO → IA u otros comandos
    response = ask_ai(message)
    bot.reply_to(message, response)
    
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Error de polling: {e}")
        time.sleep(5)  # Espera antes de reconectar