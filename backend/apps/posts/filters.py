# from django_filters import rest_framework as filters
#
# from apps.cars.choices.brand_choices import BrandChoices
#
# from .models import PostModel
#
#
# class PostFilter(filters.FilterSet):
#     year_lt = filters.NumberFilter('year', 'lt')
#     year_gt = filters.NumberFilter('year', 'gt')
#     year_range = filters.RangeFilter('year')
#     year_in = filters.BaseInFilter('year')
#     brand_contains = filters.CharFilter('brand', 'icontains')
#     body = filters.ChoiceFilter('body', choices=BrandChoices.choices)
#     order = filters.OrderingFilter(
#         fields=(
#             'id',
#             'brand',
#             'year',
#             'price',
#             'user'
#         )
#     )
#
#     class Meta:
#         model = PostModel
#         fields = ('brand', 'id', 'year')
        # fields = {
        #     'brand': ('istartswith', 'icontains'),
        #     'year': ('lt', 'gt', 'lte')
        # }
