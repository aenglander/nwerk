import logging
from typing import Callable, List

from webob import Request, Response
from webob.exc import WSGIHTTPException, HTTPInternalServerError


class Application:
    def __init__(self) -> None:
        self.__middleware_stack = []
        self.__logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, environ: dict, start_response: callable) -> List[str]:
        # noinspection PyBroadException
        try:
            response = self.__process_request(environ)
            if not isinstance(response, Response):
                self.__logger.error('Response received from middleware '
                                    'was not a Response object!')
                response = HTTPInternalServerError()
            response(environ, start_response)
            body = response.body
        except BaseException as e:
            self.__logger.critical("Server error: {}".format(e))
            start_response(u'500 Server Error',
                           [('Content-Type', 'text/plain')])
            body = b'An error occurred processing your request!'
        finally:
            # noinspection PyUnboundLocalVariable
            return [body]

    def __process_request(self, environ):
        try:
            request = Request(environ)
            response = self.__execute_middleware(request)
        except WSGIHTTPException as e:
            response = e
        return response

    def __execute_middleware(self, request: Request) -> Response:

        middleware_stack = self.__middleware_stack.copy()

        def __next_proxy(request: Request) -> Response:
            try:
                _next = middleware_stack.pop()
            except IndexError:
                _next = __terminus

            return _next(request, __next_proxy)

        def __terminus(_: Request, __: Callable) -> Response:
            pass

        try:
            response = middleware_stack.pop()(request, __next_proxy)
        except IndexError:  # No middleware
            response = None

        return response

    def append_middleware(self, middleware: Callable[
            [Request, Callable[[Request, Callable], Response]],
            Response]) -> None:
        self.__middleware_stack.append(middleware)
