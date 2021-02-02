import django_filters

from .models import *

class fteFilters(django_filters.FilterSet):
    class Meta:
        model = FTE
        fields = ['fte', 'programme', 'department', 'session', 'level']