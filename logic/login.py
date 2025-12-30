from database.db import login_user
from utils.helpers import get_user_by_telegram
from utils.validators import is_valid_dni, is_valid_pin

# ─────────────────────────────────────────────
#   FLUJO DEL LOGIN (DNI → PIN)
# ─────────────────────────────────────────────

LOGGED_IN_STATUS = 1

def login_start(msg, bot):
    """
    Initiates the login process by checking if the user is already logged in and, if not, prompts for DNI.

    Args:
        msg: The message object from the user.
        bot: The bot instance handling the message.
    """
# Verificar si ya está loggeado
    user = get_user_by_telegram(msg.from_user.id)
    if user and user[3] == LOGGED_IN_STATUS:
        bot.reply_to(msg, f"✅ Ya estás loggeado como {user[1]} del curso {user[2]}.")
        return
    
    bot.reply_to(msg, "🪪 Ingresa tu DNI:")
    bot.register_next_step_handler(msg, lambda m: ask_dni(m, bot))


def ask_dni(msg, bot):
    dni = msg.text.strip()

    if not dni.isdigit():
        bot.reply_to(msg, "❌ El DNI debe ser numérico.")
        return login_start(msg, bot)  # Reiniciar el proceso de login
    elif not is_valid_dni(dni):
        bot.reply_to(msg, "❌ El DNI debe tener entre 7 y 11 dígitos.")
        return login_start(msg, bot)  # Reiniciar el proceso de login
    bot.reply_to(msg, "🔐 Ahora ingresa tu PIN:")
    bot.register_next_step_handler(msg, lambda m: ask_pin(m, dni, bot))
def ask_pin(msg, dni, bot):
    pin = msg.text.strip()

    if not is_valid_pin(pin):
        bot.reply_to(msg, "❌ El PIN debe tener entre 4 y 6 dígitos.")
        bot.register_next_step_handler(msg, lambda m: ask_pin(m, dni, bot))
        return
    # Even though login status is checked in login_start, we call login_user here to validate credentials.
    # This ensures that the user is authenticated before proceeding.
    user = login_user(dni, pin, msg.from_user.id)
    if user:
        bot.reply_to(msg, f"✅ Bienvenido {user[1]} del curso {user[2]} 🎓")
    else:
        bot.reply_to(msg, "❌ DNI o PIN incorrectos. Vuelve a intentarlo.")
        return login_start(msg, bot)

# ─────────────────────────────────────────────
#   REGISTRO DEL COMANDO /login
# ─────────────────────────────────────────────

def register_handlers(bot):
    @bot.message_handler(commands=["login"])
    def login_handler(msg):
        login_start(msg, bot)
