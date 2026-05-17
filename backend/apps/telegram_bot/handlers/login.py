from django.contrib.auth.hashers import check_password

from students.models import Student
from telegram_bot.services.session_service import get_user_by_telegram


def login_start(msg, bot):
    student = get_user_by_telegram(msg.from_user.id)
    if student:
        bot.reply_to(msg, f'✅ Ya estás logueado como {student.nombre} del curso {student.course.name}.')
        return
    bot.reply_to(msg, '🪪 Ingresa tu DNI:')
    bot.register_next_step_handler(msg, lambda m: ask_dni(m, bot))


def ask_dni(msg, bot):
    dni = msg.text.strip()
    if not dni.isdigit() or not (7 <= len(dni) <= 11):
        bot.reply_to(msg, '❌ El DNI debe tener entre 7 y 11 dígitos numéricos.')
        return login_start(msg, bot)
    bot.reply_to(msg, '🔐 Ahora ingresa tu PIN:')
    bot.register_next_step_handler(msg, lambda m: ask_pin(m, dni, bot))


def ask_pin(msg, dni, bot):
    pin = msg.text.strip()
    if not pin.isdigit() or not (4 <= len(pin) <= 6):
        bot.reply_to(msg, '❌ El PIN debe tener entre 4 y 6 dígitos.')
        bot.register_next_step_handler(msg, lambda m: ask_pin(m, dni, bot))
        return
    try:
        student = Student.objects.get(dni=dni)
    except Student.DoesNotExist:
        bot.reply_to(msg, '❌ DNI o PIN incorrectos. Vuelve a intentarlo.')
        return login_start(msg, bot)
    if not check_password(pin, student.pin_hash):
        bot.reply_to(msg, '❌ DNI o PIN incorrectos. Vuelve a intentarlo.')
        return login_start(msg, bot)
    student.telegram_id = msg.from_user.id
    student.save()
    course_name = student.course.name if student.course else 'Sin curso'
    bot.reply_to(msg, f'✅ Bienvenido {student.nombre} del curso {course_name} 🎓')


def register_handlers(bot):
    @bot.message_handler(commands=['login'])
    def login_handler(msg):
        login_start(msg, bot)
