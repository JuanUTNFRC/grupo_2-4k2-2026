from datetime import date


class CalendarioParqueService:
    """Reglas del calendario del parque (RN3)."""

    LUNES = 0
    FERIADOS_CERRADO = {(1, 1), (12, 25)}  # (mes, día)

    def esta_abierto(self, fecha: date) -> bool:
        if (fecha.month, fecha.day) in self.FERIADOS_CERRADO:
            return False
        return fecha.weekday() != self.LUNES
