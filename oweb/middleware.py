"""App specific middleware"""
# Django imports
from django.views.defaults import page_not_found
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.template import loader
# Sekizai imports
from sekizai.context import SekizaiContext as Context
# app imports
from oweb.exceptions import OWebException, OWebAccountAccessViolation

class OWebExceptionMiddleware(object):
    """Catches OWeb specific Exceptions"""
    def process_exception(self, req, e):
        # found one of this apps exceptions
        if isinstance(e, OWebException):

            # unauthorized access to an account
            if isinstance(e, OWebAccountAccessViolation):
                t = loader.get_template('oweb/403.html')
                c = Context({'request': req})
                return HttpResponseForbidden(t.render(c))

            # handle with a 404
            return HttpResponseNotFound(
                page_not_found(req,
                    template_name='oweb/404.html')
            )
        return None
