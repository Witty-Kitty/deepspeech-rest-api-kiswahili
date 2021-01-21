from sanic.exceptions import NotFound, Unauthorized, InvalidUsage, MethodNotSupported
from sanic.response import json

from app.errors import errors_bp


@errors_bp.exception(InvalidUsage)
async def invalid_usage(request, exception):
    return json({'exception': '{}'.format(exception), 'status': exception.status_code, 'error': 'bad request'},
                status=exception.status_code)


@errors_bp.exception(Unauthorized)
async def unauthorized(request, exception):
    return json({'exception': '{}'.format(exception), 'status': exception.status_code, 'error': 'unauthorized access'},
                status=exception.status_code)


@errors_bp.exception(NotFound)
async def not_found(request, exception):
    return json({'exception': '{}'.format(exception), 'status': exception.status_code, 'error': 'not found'},
                status=exception.status_code)


@errors_bp.exception(MethodNotSupported)
async def method_not_supported(request, exception):
    return json({'exception': '{}'.format(exception), 'status': exception.status_code, 'error': 'method not supported'},
                status=exception.status_code)
