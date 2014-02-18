"""App specific middleware"""
# Django imports
from django.views.defaults import page_not_found
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.template import loader, Context
# app imports
from oweb.exceptions import OWebException, OWebSecurityIncident

class OWebExceptionMiddleware(object):
    """Catches OWeb specific Exceptions"""
    def process_exception(self, req, e):
        if isinstance(e, OWebException):
            if isinstance(e, OWebSecurityIncident):
                t = loader.get_template('oweb/404.html')
                c = Context({'foo': 'bar'})
                return HttpResponseServerError(t.render(c))
            return HttpResponseNotFound(
                page_not_found(req,
                    template_name='oweb/404.html')
            )
        return None
