from rest_framework.views import exception_handler

from core.utils import api_response


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is None:
        return None

    return api_response(
        success=False,
        message="Validation failed.",
        errors=response.data,
        status_code=response.status_code,
    )