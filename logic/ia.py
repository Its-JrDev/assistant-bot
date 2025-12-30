"""Simple placeholder AI interface used by the bot.

Provides ask_ai(message) which returns a text response. Replace with real AI integration later.
"""

from typing import Any


def ask_ai(message: Any) -> str:
    """Return a simple response based on the incoming message.

    message is the TeleBot message object; we only use message.text here.
    This is a placeholder for a real AI call.
    """
    text = (getattr(message, "text", None) or "").strip()

    if not text:
        return "No recibí texto. Escribe tu pregunta o mensaje."

    lower = text.lower()
    # simple canned replies
    if lower.startswith("hola") or "hola" in lower:
        return "¡Hola! ¿En qué puedo ayudarte hoy?"
    if "horario" in lower:
        return "Puedes consultar los horarios en la sección correspondiente o pedir que te muestre el horario de tu curso."
    if "tarea" in lower or "tareas" in lower:
        return "Para ver tus tareas usa /tareas o pregunta por la tarea específica indicando la materia."
    if text.startswith("/"):
        return "Comando no reconocido por el módulo IA. Intenta otra cosa."

    # default: echo-ish reply
    return f"He recibido tu mensaje: {text}"
