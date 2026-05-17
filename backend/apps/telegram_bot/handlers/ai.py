import os
from datetime import date

from openai import OpenAI

from academics.models import Event, Schedule, Task, Grade


_SCHOOL_SYSTEM_PROMPT = (
    "Sos un asistente educativo de un colegio. Respondé SOLO preguntas sobre "
    "el horario escolar, tareas, eventos, y notas del estudiante. "
    "Si te preguntan algo fuera de estos temas, respondé educadamente que "
    "solo podés ayudar con información escolar. "
    "No inventes información que no esté en el contexto proporcionado. "
    "No reveles datos personales del estudiante. "
    "Respondé siempre en español argentino, de forma clara y breve."
)


def _get_student_context(student) -> str:
    parts = []
    today = date.today()
    schedules = Schedule.objects.filter(course=student.course).order_by('day', 'start_time')
    if schedules:
        parts.append("HORARIO:")
        for s in schedules:
            parts.append(f"- {s.day} {s.start_time:%H:%M}-{s.end_time:%H:%M}: {s.subject}")
    tasks = Task.objects.filter(course=student.course).order_by('due_date')
    if tasks:
        parts.append("TAREAS:")
        for t in tasks:
            parts.append(f"- {t.title} ({t.subject}), vence {t.due_date:%d/%m/%Y}")
    events = Event.objects.filter(course=student.course, date__gte=today).order_by('date')
    if events:
        parts.append("EVENTOS:")
        for e in events:
            parts.append(f"- {e.title}: {e.date:%d/%m/%Y}")
    grades = Grade.objects.filter(student=student).order_by('subject', 'period')
    if grades:
        parts.append("NOTAS:")
        for g in grades:
            parts.append(f"- {g.subject} ({g.period}): {g.grade}")
    if not parts:
        return "No hay información escolar disponible para este curso."
    return "\n".join(parts)


def ask_ai(message, student=None) -> str:
    text = (getattr(message, 'text', None) or '').strip()
    if not text:
        return 'No recibí texto. Escribe tu pregunta o mensaje.'
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return '❌ El asistente IA no está configurado. Contactá al administrador.'
    client = OpenAI(
        base_url='https://openrouter.ai/api/v1',
        api_key=api_key,
    )
    context = _get_student_context(student) if student else ''
    messages = [
        {'role': 'system', 'content': _SCHOOL_SYSTEM_PROMPT},
    ]
    if context:
        messages.append({'role': 'system', 'content': f'Contexto del estudiante:\n{context}'})
    messages.append({'role': 'user', 'content': text})
    try:
        response = client.chat.completions.create(
            model='openai/gpt-4o-mini',
            messages=messages,
            max_tokens=300,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f'❌ Error al consultar el asistente: {e}'
