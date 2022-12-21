from django.contrib import admin
from handler.models import Submission, Movies, Genre, Links, Recommendations, UserRankings, FinalResult, MoviesRanked
# Register your models here.
admin.site.register(Submission)
admin.site.register(Movies)

# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.filter_vertical
# The Genre page is wonky due to the nature of many to many, so if applicable this can be implemented
# as a filter_vertical. 
admin.site.register(Genre)
admin.site.register(Links)
admin.site.register(Recommendations)
admin.site.register(FinalResult)
admin.site.register(UserRankings)
admin.site.register(MoviesRanked)