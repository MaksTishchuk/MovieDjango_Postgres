from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Movie, Actor, Genre, Rating, Category
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .forms import ReviewForm, RatingForm
from django.db.models import Q, Avg


class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year").order_by('year').distinct()


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False).prefetch_related("genres", "actors", "directors")
    template_name = "movie/movie_list.html"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Главная'
        return context


class MovieDetailView(GenreYear, DetailView):
    """Подробная информация про фильм"""
    model = Movie
    slug_field = 'url'
    template_name = "movie/movie_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        average_rating = Rating.objects.filter(movie=context['movie']).aggregate(Avg('star'))['star__avg']
        context['star_form'] = RatingForm
        context['review_form'] = ReviewForm
        if average_rating:
            context['average_rating'] = average_rating
        else:
            context['average_rating'] = 'оценок еще нет, стань первым!'
        return context


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        print(request.POST)
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.user.is_authenticated:
                form.name = self.request.user.username
                form.email = self.request.user.email
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorDetailView(GenreYear, DetailView):
    """Подробная информация об актере"""
    model = Actor
    slug_field = 'name'
    template_name = "movie/actor_detail.html"


class FilterMovieView(GenreYear, ListView):
    """Фильтрация фильмов"""
    paginate_by = 4

    def get_queryset(self):
        if self.request.GET.get('year') and not self.request.GET.get('genre'):
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist('year')),
            ).prefetch_related("genres", "actors", "directors")
        elif self.request.GET.get('genre') and not self.request.GET.get('year'):
            queryset = Movie.objects.filter(
                Q(genres__in=self.request.GET.getlist('genre'))
            ).prefetch_related("genres", "actors", "directors")
        else:
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist('year')),
                Q(genres__in=self.request.GET.getlist('genre'))
            ).prefetch_related("genres", "actors", "directors")
        return queryset.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={y}&" for y in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={g}&" for g in self.request.GET.getlist("genre")])
        context['title_page'] = 'Отфильтрованные'
        context['title_content'] = f'Результаты поиска по выбранным фильтрам'
        return context


class CategoryMovieView(GenreYear, ListView):
    """Фильтрация фильмов"""
    paginate_by = 4

    def get_queryset(self):
        queryset = Movie.objects.filter(
                Q(category__in=self.request.GET.getlist('category'))
        ).prefetch_related("genres", "actors", "directors")
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.getlist('category')
        if len(category) == 0:
            context['title_page'] = 'Фильтр по категориям'
            context['title_content'] = f'Вы не выбрали ни одной категории'
        elif len(category) != 1:
            context['title_page'] = 'Фильтр по категориям'
            context['title_content'] = f'Фильтр по выбранным категориям'
        else:
            context['title_page'] = Category.objects.get(id=int(category[0]))
            context['title_content'] = f'Результаты поиска по категории "{Category.objects.get(id=int(category[0]))}"'
        context["category"] = ''.join([f"category={c}&" for c in self.request.GET.getlist("category")])
        return context


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(GenreYear, ListView):
    """Поиск фильмов"""
    paginate_by = 4

    def get_queryset(self):
        return Movie.objects.filter(
            Q(title__icontains=self.request.GET.get('q')) |
            Q(directors__name__icontains=self.request.GET.get('q')) |
            Q(actors__name__icontains=self.request.GET.get('q'))
        ).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        context['title_page'] = f'Результаты поиска'
        context['title_content'] = f'Результаты поиска по запросу "{self.request.GET.get("q")}"'
        return context
