"""App specific middleware"""

from oweb.exceptions import OWebException

class OWebExceptionMiddleware(object):
    def process_exception(self, req, e):
        if isinstance(e, OWebException):
            raise RuntimeError('custom exception found')
        return None
