"""Provide app specific exceptions"""

class OWebException(Exception):
    """Base class for all app exceptions"""
    pass

class OWebDoesNotExist(OWebException):
    """Used, if a Django model raises its DoesNotExist Exception"""
    pass

class OWebSecurityIncident(OWebException):
    """Base class for all security related stuff"""
    pass

class OWebAccountAccessViolation(OWebSecurityIncident):
    """Used, if the authenticated user tries to access an account, that does not belong to him"""
    pass
