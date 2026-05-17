from academics.models import Grade


def get_grades(student):
    return list(Grade.objects.filter(student=student).order_by('subject', 'period'))


def format_grades(rows):
    if not rows:
        return '📝 No hay notas registradas para vos.'
    text = '📊 *Tus notas*\n'
    current_subject = None
    for g in rows:
        if g.subject != current_subject:
            text += f'\n📚 *{g.subject}*\n'
            current_subject = g.subject
        text += f'   📅 {g.period}: **{g.grade}**\n'
    return text
