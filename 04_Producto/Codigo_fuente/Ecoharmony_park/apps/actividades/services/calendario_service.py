from datetime import date


class CalendarioParqueService:
    """Reglas del calendario del parque (RN3)."""

    LUNES = 0

    def esta_abierto(self, fecha: date) -> bool:
        return fecha.weekday() != self.LUNES
