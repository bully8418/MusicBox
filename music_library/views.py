from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import *
from .forms import *
from django.db.models import Q
from hitcount.views import HitCountDetailView


class Search(ListView):
    model = Song
    template_name = 'search_result.html'
    context_object_name = 'search'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        object_list = Song.objects.filter(
            Q(name__icontains=query) | Q(artist__name__icontains=query.capitalize()) | Q(album__name__icontains=query)
        )
        return object_list

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


# main page where all music and content
class SongView(ListView):
    queryset = Song.objects.order_by('-date')[:3]
    template_name = 'base_page.html'
    context_object_name = 'music'


class SongDetailView(HitCountDetailView):
    model = Song
    template_name = 'song_detail.html'
    context_object_name = 'rate'
    pk_url_kwarg = 'pk'
    # set to True to count the hit
    count_hit = True
    slug_field = "url"

    # def get_context_data(self, **kwargs):
    #     # context = super(SongDetailView, self).get_context_data(**kwargs)
    #     # context.update({
    #     #     'popular_songs': Song.objects.order_by('-hit_count_generic__hits')[:3],
    #     # })
    #     # return context
    #     context = super().get_context_data(**kwargs)
    #     context["star_form"] = RatingForm()
    #     return context


class ArtistView(DetailView):
    model = Artist
    template_name = 'artist_page.html'
    context_object_name = 'artist_info'


class AlbumsView(ListView):
    model = Album
    template_name = 'albums_list.html'
    context_object_name = 'album_list'


class ArtistsView(ListView):
    model = Artist
    template_name = 'artists_list.html'
    context_object_name = 'artists'


class AlbumDetailView(HitCountDetailView):
    model = Album
    template_name = 'album_page.html'
    context_object_name = 'album_info'
    pk_url_kwarg = 'pk'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        context.update({
            'popular_albums': Album.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context


# class AddStarRating(View):
#     """???????????????????? ???????????????? ??????????"""
#     def get_client_ip(self, request):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip
#
#     def post(self, request):
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             Rating.objects.update_or_create(
#                 ip=self.get_client_ip(request),
#                 song_id=int(request.POST.get("song")),
#                 defaults={'star_id': int(request.POST.get("star"))}
#             )
#             return HttpResponse(status=201)
#         else:
#             return HttpResponse(status=400)