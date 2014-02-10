# charset: utf-8
"""Hooks this app into the Django admin backend"""

from django.contrib import admin
from oweb.models import *

admin.site.register(Account)
