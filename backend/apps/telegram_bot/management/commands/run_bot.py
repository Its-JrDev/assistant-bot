import os
import time
import telebot

from django.core.management.base import BaseCommand

from telegram_bot.handlers.login import register_handlers as register_login
from telegram_bot.handlers.logout import register_handlers as register_logout
from telegram_bot.handlers.schedules import format_schedule, get_schedule
from telegram_bot.handlers.ai import ask_ai
from telegram_bot.services.session_service import get_user_by_telegram


class Command(BaseCommand):
    help = 'Starts the Telegram bot in polling mode'

    def handle(self, *args, **options):
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            self.stderr.write('TELEGRAM_BOT_TOKEN environment variable not set')
            return

        bot = telebot.TeleBot(token)

        register_login(bot)
        register_logout(bot)

        @bot.message_handler(commands=['start'])
        def start(message):
            bot.reply_to(message, 'Bienvenido al asistente escolar. Usa /login para identificarte.')

        @bot.message_handler(commands=['horario'])
        def horario_handler(message):
            user = get_user_by_telegram(message.from_user.id)
            if not user:
                bot.reply_to(message, '🔒 Necesitas iniciar sesión con /login para ver tu horario.')
                return
            if user[3] != 1:
                bot.reply_to(message, '🔒 Tu sesión no está activa. Usa /login.')
                return
            rows = get_schedule(user[2])
            bot.reply_to(message, format_schedule(rows), parse_mode='Markdown')

        @bot.message_handler(func=lambda msg: True)
        def main_handler(message):
            if message.text.startswith('/') or message.text.isdigit():
                return
            user = get_user_by_telegram(message.from_user.id)
            if not user:
                bot.reply_to(message, '🔒 Necesitas iniciar sesión con /login para usar el asistente.')
                return
            if user[3] != 1:
                bot.reply_to(message, '🔒 Tu sesión no está activa. Usa /login.')
                return
            response = ask_ai(message)
            bot.reply_to(message, response)

        self.stdout.write('Bot started polling...')
        while True:
            try:
                bot.infinity_polling(timeout=60, long_polling_timeout=60)
            except Exception as e:
                self.stderr.write(f'Error de polling: {e}')
                time.sleep(5)
