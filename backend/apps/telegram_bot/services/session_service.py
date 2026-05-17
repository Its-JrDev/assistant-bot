from students.models import Student


def get_user_by_telegram(tid):
    try:
        return Student.objects.get(telegram_id=tid)
    except Student.DoesNotExist:
        return None
