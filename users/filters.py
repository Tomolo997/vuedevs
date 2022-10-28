import django_filters

from .models import *

class DeveloperFilter(django_filters.FilterSet):
    class Meta:
        model = Developer
        fields = ['name','timezone']
