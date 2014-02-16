"""App specific middleware"""
# Django imports
from django.views.defaults import page_not_found
from django.http import HttpResponseNotFound
# app imports
from oweb.exceptions import OWebException

class OWebExceptionMiddleware(object):
    """Catches OWeb specific Exceptions"""
    def process_exception(self, req, e):
        if isinstance(e, OWebException):
            return HttpResponseNotFound(
                page_not_found(req,
                    template_name='oweb/404.html')
            )
        return None
