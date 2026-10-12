from datetime import date, datetime, time, timedelta


class CalendarioParqueService:
    """Reglas del calendario del parque (RN3)."""

    LUNES = 0
    APERTURA = time(8, 30)
    CIERRE = time(19, 0)
    DURACION_ACTIVIDAD = timedelta(hours=1)
    FERIADOS_CERRADO = {(1, 1), (12, 25)}  # (mes, día)

    def esta_abierto(self, fecha: date) -> bool:
        if (fecha.month, fecha.day) in self.FERIADOS_CERRADO:
            return False
        return fecha.weekday() != self.LUNES

    def admite_actividad(self, fecha: date, hora_inicio: time) -> bool:
        inicio = datetime.combine(fecha, hora_inicio)
        fin = inicio + self.DURACION_ACTIVIDAD
        return (
            hora_inicio >= self.APERTURA
            and fin <= datetime.combine(fecha, self.CIERRE)
        )
