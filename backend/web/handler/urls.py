from django.urls import path
from handler import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/submissions/', views.Submissions_list.as_view()),
    path('api/submissions/<int:pk>/', views.Submissions_detail.as_view()),
    path('api/movies/', views.Movie_list.as_view()),
    path('api/movies/<int:pk>/', views.Movie_detail.as_view()),
    path('api/movies/random/', views.movie_random),
    path('api/movies/random_image/', views.movie_random_image),
    path('api/movies/random/5/', views.Movie_random_list.as_view()),
    path('api/movies/random/1/', views.movie_random_new),
    path('api/movies/image/<int:pk>', views.movie_get_image),
    path('api/submissions/rating/', views.Rating.as_view()),
    path('api/recommendation/<str:pk>/<str:pk_model>', views.Recommendation.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)