from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    """Respuestas de error con formato uniforme: {"codigo": ..., "detalle": ...}.

    DRF arma la respuesta con el status de la excepción; acá solo cambia el formato.
    Los errores de formato del serializer suman "errores" con el detalle por campo.
    """
    response = drf_exception_handler(exc, context)
    if response is None:
        return response

    if isinstance(exc, ValidationError):
        response.data = {
            'codigo': 'datos_invalidos',
            'detalle': 'Los datos enviados no son válidos.',
            'errores': response.data,
        }
    elif 'detail' in response.data:
        detalle = response.data['detail']
        response.data = {'codigo': detalle.code, 'detalle': str(detalle)}
    return response
