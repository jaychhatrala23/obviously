from datetime import date

from django_filters import rest_framework as filters

from person.models import Person


class PersonFilter(filters.FilterSet):
    """
    Filter class to handle filtering of Person queryset.
    """
    age = filters.NumberFilter(method='filter_by_age')

    class Meta:
        model = Person
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
        }

    def filter_by_age(self, queryset, name, value):
        """
        Custom method to filter by age.
        """
        today = date.today()
        birth_year = today.year - int(value)
        birth_date_after = date(birth_year, today.month, today.day)
        birth_date_before = date(birth_year + 1, today.month, today.day)
        return queryset.filter(date_of_birth__gte=birth_date_after,
                               date_of_birth__lt=birth_date_before)