import os
import time
import telebot

from django.core.management.base import BaseCommand

from telegram_bot.handlers.login import register_handlers as register_login
from telegram_bot.handlers.logout import register_handlers as register_logout
from telegram_bot.handlers.schedules import format_schedule, get_schedule
from telegram_bot.handlers.tasks import format_tasks, get_tasks
from telegram_bot.handlers.events import format_events, get_events
from telegram_bot.handlers.notas import format_grades, get_grades
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
            student = get_user_by_telegram(message.from_user.id)
            if not student:
                bot.reply_to(message, '🔒 Necesitas iniciar sesión con /login para ver tu horario.')
                return
            if not student.course:
                bot.reply_to(message, '⚠️ No estás asignado a ningún curso.')
                return
            rows = get_schedule(student.course)
            bot.reply_to(message, format_schedule(rows), parse_mode='Markdown')

        @bot.message_handler(commands=['tareas'])
        def tareas_handler(message):
            student = get_user_by_telegram(message.from_user.id)
            if not student:
                bot.reply_to(message, '🔒 Necesitas iniciar sesión con /login para ver tus tareas.')
                return
            if not student.course:
                bot.reply_to(message, '⚠️ No estás asignado a ningún curso.')
                return
            rows = get_tasks(student.course)
            bot.reply_to(message, format_tasks(rows), parse_mode='Markdown')

        @bot.message_handler(commands=['eventos'])
        def eventos_handler(message):
            student = get_user_by_telegram(message.from_user.id)
            if not student:
                bot.reply_to(message, '🔒 Necesitas iniciar sesión con /login para ver los eventos.')
                return
            if not student.course:
                bot.reply_to(message, '⚠️ No estás asignado a ningún curso.')
                return
            rows = get_events(student.course)
            bot.reply_to(message, format_events(rows), parse_mode='Markdown')

        @bot.message_handler(commands=['notas'])
        def notas_handler(message):
            student = get_user_by_telegram(message.from_user.id)
            if not student:
                bot.reply_to(message, '🔒 Necesitas iniciar sesión con /login para ver tus notas.')
                return
            rows = get_grades(student)
            bot.reply_to(message, format_grades(rows), parse_mode='Markdown')

        @bot.message_handler(func=lambda msg: True)
        def main_handler(message):
            if message.text.startswith('/') or message.text.isdigit():
                return
            student = get_user_by_telegram(message.from_user.id)
            if not student:
                bot.reply_to(message, '🔒 Necesitas iniciar sesión con /login para usar el asistente.')
                return
            response = ask_ai(message, student=student)
            bot.reply_to(message, response)

        self.stdout.write('Bot started polling...')
        while True:
            try:
                bot.infinity_polling(timeout=60, long_polling_timeout=60)
            except Exception as e:
                self.stderr.write(f'Error de polling: {e}')
                time.sleep(5)
