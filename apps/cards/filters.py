import django_filters

from apps.cards.models import Card


class CardFilter(django_filters.FilterSet):
    categories_id = django_filters.Filter(method='filter_by_category')

    class Meta:
        model = Card
        fields = ['categories']

    def filter_by_category(self, queryset, name, value):
        categories_id = value

        for category_id in categories_id:
            queryset = queryset.filter(categories__id=category_id)

        return queryset
