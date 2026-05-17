"""Simple placeholder AI interface used by the bot.
Provides ask_ai(message) which returns a text response.
Replace with real AI integration in F2 (bot-refactor).
"""


def ask_ai(message) -> str:
    text = (getattr(message, 'text', None) or '').strip()
    if not text:
        return 'No recibí texto. Escribe tu pregunta o mensaje.'
    lower = text.lower()
    if 'hola' in lower:
        return '¡Hola! ¿En qué puedo ayudarte hoy?'
    if 'horario' in lower:
        return 'Puedes consultar los horarios con el comando /horario.'
    if 'tarea' in lower:
        return 'Para ver tus tareas usa /tareas o pregunta por la materia.'
    if text.startswith('/'):
        return 'Comando no reconocido.'
    return f'He recibido tu mensaje: {text}'
