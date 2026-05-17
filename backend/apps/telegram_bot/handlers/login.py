from database.db import login_user
from telegram_bot.services.session_service import get_user_by_telegram
from telegram_bot.handlers.schedules import is_valid_dni, is_valid_pin

LOGGED_IN_STATUS = 1


def login_start(msg, bot):
    user = get_user_by_telegram(msg.from_user.id)
    if user and user[3] == LOGGED_IN_STATUS:
        bot.reply_to(msg, f'✅ Ya estás loggeado como {user[1]} del curso {user[2]}.')
        return
    bot.reply_to(msg, '🪪 Ingresa tu DNI:')
    bot.register_next_step_handler(msg, lambda m: ask_dni(m, bot))


def ask_dni(msg, bot):
    dni = msg.text.strip()
    if not dni.isdigit():
        bot.reply_to(msg, '❌ El DNI debe ser numérico.')
        return login_start(msg, bot)
    if not is_valid_dni(dni):
        bot.reply_to(msg, '❌ El DNI debe tener entre 7 y 11 dígitos.')
        return login_start(msg, bot)
    bot.reply_to(msg, '🔐 Ahora ingresa tu PIN:')
    bot.register_next_step_handler(msg, lambda m: ask_pin(m, dni, bot))


def ask_pin(msg, dni, bot):
    pin = msg.text.strip()
    if not is_valid_pin(pin):
        bot.reply_to(msg, '❌ El PIN debe tener entre 4 y 6 dígitos.')
        bot.register_next_step_handler(msg, lambda m: ask_pin(m, dni, bot))
        return
    user = login_user(dni, pin, msg.from_user.id)
    if user:
        bot.reply_to(msg, f'✅ Bienvenido {user[1]} del curso {user[2]} 🎓')
    else:
        bot.reply_to(msg, '❌ DNI o PIN incorrectos. Vuelve a intentarlo.')
        return login_start(msg, bot)


def register_handlers(bot):
    @bot.message_handler(commands=['login'])
    def login_handler(msg):
        login_start(msg, bot)
