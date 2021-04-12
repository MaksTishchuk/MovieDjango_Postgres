from django.urls import path
from . import views

urlpatterns = [
    path('', views.MoviesView.as_view(), name='movies_list'),
    path('filter/', views.FilterMovieView.as_view(), name='filter'),
    path('on_category/', views.CategoryMovieView.as_view(), name='category'),
    path('search/', views.Search.as_view(), name='search'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path('film/<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('actor/<str:slug>/', views.ActorDetailView.as_view(), name='actor_detail'),
]