"""Provide app specific exceptions"""

class OWebException(Exception):
    """Base class for all app exceptions"""
    pass

class OWebDoesNotExist(OWebException):
    """Used, if a Django model raises its DoesNotExist Exception"""
    pass
