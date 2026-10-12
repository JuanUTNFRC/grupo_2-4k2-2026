from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    """Respuestas de error con formato uniforme: {"codigo": ..., "detalle": ...}.

    DRF arma la respuesta con el status de la excepción; acá solo cambia el formato.
    """
    response = drf_exception_handler(exc, context)
    if response is None or 'detail' not in response.data:
        return response

    detalle = response.data['detail']
    response.data = {'codigo': detalle.code, 'detalle': str(detalle)}
    return response
