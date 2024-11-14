import django_filters

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from apps.cards.models import Card


class CardFilter(django_filters.FilterSet):
    query = django_filters.Filter(method='card_search')
    categories_id = django_filters.Filter(method='filter_by_category')

    class Meta:
        model = Card
        fields = ['categories']

    def card_search(self, queryset, name, value):
        vector = SearchVector('word', 'translation', 'example')
        query = SearchQuery(value)

        queryset = queryset.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001).order_by('-rank')

        return queryset

    def filter_by_category(self, queryset, name, value):
        categories_id = value

        for category_id in categories_id:
            queryset = queryset.filter(categories__id=category_id)

        return queryset
