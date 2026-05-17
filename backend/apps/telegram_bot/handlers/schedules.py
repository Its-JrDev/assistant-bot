from academics.models import Schedule


def get_schedule(course):
    return list(Schedule.objects.filter(course=course).order_by('day', 'start_time'))


def format_schedule(rows):
    if not rows:
        return '❌ No hay horario cargado para tu curso.'
    text = '📚 *Horario semanal*\n'
    current_day = None
    for sched in rows:
        if sched.day != current_day:
            text += f'\n📆 *{sched.day}*\n'
            current_day = sched.day
        text += f'🕒 {sched.start_time:%H:%M}-{sched.end_time:%H:%M} — *{sched.subject}*'
        if sched.teacher_name:
            text += f' ({sched.teacher_name})'
        text += '\n'
    return text
