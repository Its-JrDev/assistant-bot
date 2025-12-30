def is_valid_dni(dni: str) -> bool:
    """Valida que el DNI tenga solo números y de 7 a 11 dígitos."""
    return dni.isdigit() and 7<= len(dni) <= 11

def is_valid_pin(pin: str) -> bool:
    """PIN de 4 a 6 dígitos numéricos."""
    return pin.isdigit() and 4 <= len(pin) <= 6

def is_logged(user):
    """Valida si una instancia de usuario está loggeada."""
    return user and user[3] == 1  # depende de la estructura de DB

def not_empty(text: str) -> bool:
    """Verifica que no esté vacío."""
    return bool(text and text.strip())
