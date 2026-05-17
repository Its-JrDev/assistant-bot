from telegram_bot.services.session_service import get_user_by_telegram


def logout(msg, bot):
    student = get_user_by_telegram(msg.from_user.id)
    if not student:
        bot.reply_to(msg, 'ℹ️ No tienes una sesión activa.')
        return
    student.telegram_id = None
    student.save()
    bot.reply_to(msg, '🔓 Has cerrado sesión correctamente.')


def register_handlers(bot):
    @bot.message_handler(commands=['logout'])
    def logout_handler(msg):
        logout(msg, bot)
