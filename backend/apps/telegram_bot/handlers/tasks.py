from datetime import date

from academics.models import Task


def get_tasks(course):
    return list(Task.objects.filter(course=course).order_by('due_date'))


def format_tasks(rows):
    if not rows:
        return '✅ No hay tareas pendientes para tu curso.'
    text = '📋 *Tareas pendientes*\n'
    for t in rows:
        text += f'\n📌 *{t.title}* ({t.subject})\n'
        text += f'   📅 Vence: {t.due_date:%d/%m/%Y}\n'
        if t.description:
            text += f'   {t.description}\n'
    return text
