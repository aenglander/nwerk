"""
This is a super simple WSGI application example for uWSGI.
It creates a middleware function, creates an Application,
and then appends the middleware.

The application attribute of the module will be automatically picked up by
uWSGI as the application
"""
from typing import Callable
from nwerk.application import Application
from webob import Response, Request


def _hello_middleware(_request: Request, _next: Callable) -> Response:
    return Response('Hello, World!', content_type='text/plain')


application = Application()
application.append_middleware(_hello_middleware)
