from database.db import logout_user
from utils.helpers import get_user_by_telegram

def logout(msg, bot):
    user = get_user_by_telegram(msg.from_user.id)

    if not user or user[3] != 1:
        bot.reply_to(msg, "ℹ️ No tienes una sesión activa.")
        return

    success = logout_user(msg.from_user.id)

    if success:
        bot.reply_to(msg, "🔓 Has cerrado sesión correctamente.")
    else:
        bot.reply_to(msg, "❌ Ocurrió un error al cerrar sesión.")

def register_handlers(bot):
    @bot.message_handler(commands=["logout"])
    def logout_handler(msg):
        logout(msg, bot)