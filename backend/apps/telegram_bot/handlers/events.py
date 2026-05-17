from datetime import date

from academics.models import Event


def get_events(course):
    return list(Event.objects.filter(course=course, date__gte=date.today()).order_by('date'))


def format_events(rows):
    if not rows:
        return '🎉 No hay eventos próximos para tu curso.'
    text = '📅 *Próximos eventos*\n'
    for e in rows:
        text += f'\n🎯 *{e.title}*\n'
        text += f'   📆 {e.date:%d/%m/%Y}\n'
        if e.description:
            text += f'   {e.description}\n'
    return text
