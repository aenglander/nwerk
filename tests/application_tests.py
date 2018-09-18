import logging
import unittest
from typing import Callable
from unittest.mock import MagicMock, ANY, call, patch

from nwerk.application import Application
from webob import Request, Response


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.__app = Application()
        self.__request = Request.blank('/')
        logging.getLogger(Application.__name__).disabled = True

    def tearDown(self):
        del self.__app, self.__request

    def test_no_middleware_generates_500_response(self):
        response = self.__request.get_response(self.__app)
        self.assertEqual(500, response.status_code)

    def test_middleware_response_body_is_returned(self):
        expected = b"Expected Body"

        def _middleware(_: Request, _next: Callable) -> Response:
            return Response(expected)

        self.__app.append_middleware(_middleware)
        actual = self.__request.get_response(self.__app).body
        self.assertEqual(actual, expected)

    def test_middleware_response_status_is_returned(self):
        expected = "204 No Content"

        def _middleware(_: Request, _next: Callable) -> Response:
            return Response(status=expected)

        self.__app.append_middleware(_middleware)
        actual = self.__request.get_response(self.__app).status
        self.assertEqual(actual, expected)

    def test_middleware_headers_are_returned(self):
        def _middleware(_: Request, _next: Callable) -> Response:
            return Response(headers=[('X-OMG', 'Oh My Goodness!')])

        self.__app.append_middleware(_middleware)
        actual = self.__request.get_response(self.__app).headers
        self.assertIn('X-OMG', actual, 'Header missing')
        self.assertEqual(actual['X-OMG'], 'Oh My Goodness!',
                         'Incorrect header value')

    def test_middleware_items_are_called_in_order(self):
        def _middleware(request: Request, _next: Callable) -> Response:
            _next(request)
            return Response()

        mock = MagicMock()
        mock.middleware_one.side_effect = _middleware
        self.__app.append_middleware(mock.middleware_one)
        mock.middleware_two.side_effect = _middleware
        self.__app.append_middleware(mock.middleware_two)
        mock.middleware_three.side_effect = _middleware
        self.__app.append_middleware(mock.middleware_three)
        mock.middleware_four.side_effect = _middleware
        self.__app.append_middleware(mock.middleware_four)
        mock.middleware_five.side_effect = _middleware
        self.__app.append_middleware(mock.middleware_five)
        self.__request.get_response(self.__app)
        mock.assert_has_calls(
            [call.middleware_five(ANY, ANY), call.middleware_four(ANY, ANY),
             call.middleware_three(ANY, ANY), call.middleware_two(ANY, ANY),
             call.middleware_one(ANY, ANY)])

    @patch.object(Request, '__init__', return_value=None)
    def test_request_created_with_proper_environment(self, request_init_patch):
        self.__request.get_response(self.__app)
        request_init_patch.assert_called_once_with(self.__request.environ)

    def test_last_middleware_receives_none_as_response(self):
        class Middleware:
            def __init__(self):
                self.called = False
                self.actual = 'Not None'

            def __call__(self, request: Request, _next: Callable) -> Response:
                self.actual = _next(request)
                self.called = True
                return Response()

        middleware = Middleware()
        self.__app.append_middleware(middleware)
        self.__request.get_response(self.__app)
        self.assertTrue(middleware.called, 'Middleware was never called')
        self.assertIsNone(middleware.actual)

    def test_middleware_proxy_returns_upstream_response(self):
        def _middleware(request: Request, _next: Callable) -> Response:
            response = _next(request)
            body = b'step' if response is None else b'step + ' + response.body
            return Response(body)

        self.__app.append_middleware(_middleware)
        self.__app.append_middleware(_middleware)
        self.__app.append_middleware(_middleware)
        actual =  self.__request.get_response(self.__app).body
        self.assertEqual(actual, b'step + step + step')
