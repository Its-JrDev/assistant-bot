from unittest.mock import MagicMock, patch
from datetime import date, time

from django.test import TestCase
from django.contrib.auth.hashers import make_password

from students.models import Student
from academics.models import Course, Schedule, Task, Event, Grade
from telegram_bot.services.session_service import get_user_by_telegram
from telegram_bot.handlers.login import login_start, ask_dni, ask_pin
from telegram_bot.handlers.logout import logout
from telegram_bot.handlers.schedules import get_schedule, format_schedule
from telegram_bot.handlers.tasks import get_tasks, format_tasks
from telegram_bot.handlers.events import get_events, format_events
from telegram_bot.handlers.notas import get_grades, format_grades


def _make_msg(text, user_id=12345):
    msg = MagicMock()
    msg.text = text
    msg.from_user.id = user_id
    return msg


class SessionServiceTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='1A', academic_year=2026)

    def test_get_user_by_telegram_found(self):
        student = Student.objects.create(
            dni='12345678', pin_hash=make_password('4321'),
            nombre='Alumno Test', course=self.course, telegram_id=999
        )
        result = get_user_by_telegram(999)
        self.assertEqual(result, student)

    def test_get_user_by_telegram_not_found(self):
        result = get_user_by_telegram(999)
        self.assertIsNone(result)


class LoginHandlerTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='1A', academic_year=2026)
        self.student = Student.objects.create(
            dni='12345678', pin_hash=make_password('4321'),
            nombre='Alumno Test', course=self.course,
        )

    def test_login_start_already_logged(self):
        self.student.telegram_id = 12345
        self.student.save()
        bot = MagicMock()
        msg = _make_msg('/login', user_id=12345)
        login_start(msg, bot)
        bot.reply_to.assert_called_once()
        args = bot.reply_to.call_args[0]
        self.assertIn('Ya estás logueado', args[1])

    def test_login_start_asks_dni(self):
        bot = MagicMock()
        msg = _make_msg('/login', user_id=99999)
        login_start(msg, bot)
        bot.reply_to.assert_called_once_with(msg, '🪪 Ingresa tu DNI:')
        bot.register_next_step_handler.assert_called_once()

    def test_ask_dni_invalid_short(self):
        bot = MagicMock()
        msg = _make_msg('123', user_id=99999)
        ask_dni(msg, bot)
        calls = [c[0][1] for c in bot.reply_to.call_args_list]
        self.assertTrue(any('debe tener entre 7 y 11' in c for c in calls))

    def test_ask_dni_valid(self):
        bot = MagicMock()
        msg = _make_msg('12345678', user_id=99999)
        ask_dni(msg, bot)
        bot.reply_to.assert_called_once_with(msg, '🔐 Ahora ingresa tu PIN:')
        bot.register_next_step_handler.assert_called_once()

    def test_ask_pin_invalid_short(self):
        bot = MagicMock()
        msg = _make_msg('12', user_id=99999)
        ask_pin(msg, '12345678', bot)
        bot.reply_to.assert_called()
        self.assertIn('debe tener entre 4 y 6', bot.reply_to.call_args[0][1])

    def test_ask_pin_wrong_dni(self):
        bot = MagicMock()
        msg = _make_msg('4321', user_id=99999)
        ask_pin(msg, '00000000', bot)
        calls = [c[0][1] for c in bot.reply_to.call_args_list]
        self.assertTrue(any('incorrectos' in c for c in calls))

    def test_ask_pin_wrong_pin(self):
        bot = MagicMock()
        msg = _make_msg('9999', user_id=99999)
        ask_pin(msg, '12345678', bot)
        calls = [c[0][1] for c in bot.reply_to.call_args_list]
        self.assertTrue(any('incorrectos' in c for c in calls))

    def test_ask_pin_success(self):
        bot = MagicMock()
        msg = _make_msg('4321', user_id=99999)
        ask_pin(msg, '12345678', bot)
        bot.reply_to.assert_called_once()
        args = bot.reply_to.call_args[0]
        self.assertIn('Bienvenido', args[1])
        self.student.refresh_from_db()
        self.assertEqual(self.student.telegram_id, 99999)


class LogoutHandlerTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='1A', academic_year=2026)

    def test_logout_no_session(self):
        bot = MagicMock()
        msg = _make_msg('/logout', user_id=99999)
        logout(msg, bot)
        bot.reply_to.assert_called_once()
        self.assertIn('No tienes una sesión activa', bot.reply_to.call_args[0][1])

    def test_logout_success(self):
        student = Student.objects.create(
            dni='12345678', pin_hash='', nombre='Test',
            course=self.course, telegram_id=99999
        )
        bot = MagicMock()
        msg = _make_msg('/logout', user_id=99999)
        logout(msg, bot)
        bot.reply_to.assert_called_once()
        self.assertIn('Has cerrado sesión', bot.reply_to.call_args[0][1])
        student.refresh_from_db()
        self.assertIsNone(student.telegram_id)


class SchedulesHandlerTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='1A', academic_year=2026)
        Schedule.objects.create(
            course=self.course, day='Lunes',
            start_time=time(8, 0), end_time=time(9, 0),
            subject='Matemáticas', teacher_name='Prof. García'
        )

    def test_get_schedule(self):
        rows = get_schedule(self.course)
        self.assertEqual(len(rows), 1)

    def test_format_schedule(self):
        rows = get_schedule(self.course)
        text = format_schedule(rows)
        self.assertIn('Lunes', text)
        self.assertIn('Matemáticas', text)
        self.assertIn('Prof. García', text)

    def test_format_schedule_empty(self):
        text = format_schedule([])
        self.assertIn('No hay horario', text)


class TasksHandlerTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='1A', academic_year=2026)
        Task.objects.create(
            course=self.course, subject='Matemáticas',
            title='TP Nº1', description='Resolver ejercicios',
            due_date='2026-06-01'
        )

    def test_get_tasks(self):
        rows = get_tasks(self.course)
        self.assertEqual(len(rows), 1)

    def test_format_tasks(self):
        rows = get_tasks(self.course)
        text = format_tasks(rows)
        self.assertIn('TP Nº1', text)
        self.assertIn('01/06/2026', text)

    def test_format_tasks_empty(self):
        text = format_tasks([])
        self.assertIn('No hay tareas', text)


class EventsHandlerTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='1A', academic_year=2026)

    def test_get_events(self):
        Event.objects.create(
            course=self.course, title='Acto fin de año',
            date='2026-12-20'
        )
        rows = get_events(self.course)
        self.assertEqual(len(rows), 1)

    def test_get_events_skips_past(self):
        Event.objects.create(
            course=self.course, title='Evento pasado',
            date='2020-01-01'
        )
        rows = get_events(self.course)
        self.assertEqual(len(rows), 0)

    def test_format_events(self):
        Event.objects.create(
            course=self.course, title='Acto fin de año',
            date='2026-12-20', description='En el patio'
        )
        rows = get_events(self.course)
        text = format_events(rows)
        self.assertIn('Acto fin de año', text)
        self.assertIn('En el patio', text)

    def test_format_events_empty(self):
        text = format_events([])
        self.assertIn('No hay eventos', text)


class NotasHandlerTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='1A', academic_year=2026)
        self.student = Student.objects.create(
            dni='12345678', pin_hash='', nombre='Test',
            course=self.course,
        )

    def test_get_grades(self):
        Grade.objects.create(
            student=self.student, subject='Matemáticas',
            grade=8.5, period='Trimestre 1'
        )
        rows = get_grades(self.student)
        self.assertEqual(len(rows), 1)

    def test_format_grades(self):
        Grade.objects.create(
            student=self.student, subject='Matemáticas',
            grade=8.5, period='Trimestre 1'
        )
        rows = get_grades(self.student)
        text = format_grades(rows)
        self.assertIn('Matemáticas', text)
        self.assertIn('8.5', text)

    def test_format_grades_empty(self):
        text = format_grades([])
        self.assertIn('No hay notas', text)


class AIHandlerTest(TestCase):
    @patch('telegram_bot.handlers.ai.OpenAI')
    def test_ask_ai_no_api_key(self, mock_openai):
        from telegram_bot.handlers.ai import ask_ai
        with patch('telegram_bot.handlers.ai.os.getenv', return_value=None):
            msg = _make_msg('Hola')
            response = ask_ai(msg)
            self.assertIn('no está configurado', response)

    @patch('telegram_bot.handlers.ai.os.getenv', return_value='sk-test')
    @patch('telegram_bot.handlers.ai.OpenAI')
    def test_ask_ai_empty_text(self, mock_openai, mock_getenv):
        msg = _make_msg('')
        from telegram_bot.handlers.ai import ask_ai
        response = ask_ai(msg)
        self.assertIn('No recibí texto', response)
