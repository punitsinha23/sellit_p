import os
import django
from django.core.wsgi import get_wsgi_application
from werkzeug.wrappers import Response

# Set up the Django settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")
django.setup()

# Get the WSGI application.
application = get_wsgi_application()

def handler(request, context):
    """
    Vercel calls this function to handle requests.
    """
    # Copy the request’s environment.
    environ = request.environ.copy()

    # Container for capturing status and headers.
    response_status = None
    response_headers = None

    def start_response(status, headers, exc_info=None):
        nonlocal response_status, response_headers
        response_status = status
        response_headers = headers

    # Call Django's WSGI application.
    result = application(environ, start_response)
    response_body = b"".join(result)
    
    # Parse status code from e.g. "200 OK".
    status_code = int(response_status.split()[0])
    headers_dict = dict(response_headers)

    return Response(response_body, status=status_code, headers=headers_dict)
