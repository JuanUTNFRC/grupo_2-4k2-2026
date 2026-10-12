from datetime import date


class CalendarioParqueService:
    """Reglas del calendario del parque (RN3)."""

    def esta_abierto(self, fecha: date) -> bool:
        return True
