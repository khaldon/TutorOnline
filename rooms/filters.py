import django_filters
from .models import Room
class RoomFilter(django_filters.FilterSet):
    CHOICES = (
        ('ascending','Ascending'),
        ('descending', 'Descending')
    )
    ordering = django_filters.ChoiceFilter(label='ordering', choices=CHOICES, method='filter_by_order')
    class Meta:
        model = Room
        fields = {
            'title':['icontains']
        }

    def filter_by_order(self, queryset, name, value):
        expression  = 'created' if value == 'ascending' else '-created'
        return queryset.order_by(expression)        
