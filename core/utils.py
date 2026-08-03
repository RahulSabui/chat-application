from datetime import datetime
from rest_framework.response import Response


def api_response(
    *,
    success=True,
    message="Success",
    data=None,
    errors=None,
    status_code=200,
):

    return Response(
        {
            "success": success,
            "status": status_code,
            "message": message,
            "data": data,
            "errors": errors,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
        status=status_code,
    )