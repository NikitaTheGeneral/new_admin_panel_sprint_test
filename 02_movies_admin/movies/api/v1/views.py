from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.core.paginator import Paginator

from movies.models import Filmwork

class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        mydata = Filmwork.objects.values('id', 'title', 'description', 'creation_date', 'rating', 'type').annotate(genres=ArrayAgg('genres__name', distinct=True),
                                                                                                                   actors=ArrayAgg('personfilmwork__person__full_name', filter=Q(personfilmwork__role='actor'), distinct=True),
                                                                                                                   directors=ArrayAgg('personfilmwork__person__full_name', filter=Q(personfilmwork__role='director'), distinct=True),
                                                                                                                   writers=ArrayAgg('personfilmwork__person__full_name', filter=Q(personfilmwork__role='writer'), distinct=True))
        return mydata

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)

class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        prevpage = None
        nextpage = None
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        if page.has_previous() and page.has_next():
            prevpage = page.previous_page_number()
            nextpage = page.next_page_number()
        elif page.has_previous():
            prevpage = page.previous_page_number()
        elif page.has_next():
            nextpage = page.next_page_number()

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': prevpage,
            'next': nextpage,
            'results': list(queryset),
            }
        return context

class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        context = self.get_object(queryset=queryset)
        return context