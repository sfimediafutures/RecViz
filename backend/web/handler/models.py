from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Submission(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    userId = models.CharField(max_length=100)
    answers = models.JSONField()
    pageId = models.CharField(max_length=100)    

    # boolean for signal and interlan logic
    train_on_submission = models.BooleanField(default=False)
    final_submission = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        
    def __str__(self):
        return f'{self.userId} on form {self.pageId}'

# Example Models from movielens-latest-small dataset:
# We are only intrested in moves and links.
class MoviesRanked(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey("handler.Movies", on_delete=models.CASCADE)
    tmdbId = models.IntegerField()
    rank = models.IntegerField()
    cached_img_url = models.CharField(default='not_cached', max_length=400)
    cached_background_img_url = models.CharField(default='not_cached', max_length=400)
    
class Movies(models.Model):
    movieId = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    # add popularity
    class Meta:
        ordering = ['movieId']
    
    # same as going genre_set.all() on movie object.
    def genre(self):
        self.genre = self.genre_set.all()
        return self.genre  

    def links(self):
        self.links = self.links_set.all()
        return self.links

    def __str__(self): 
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=200)
    # this way you can access all movies related to Genre: 
    # Genre.objects.get(name='Action').movie.all()
    movies = models.ManyToManyField(Movies)
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Links(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    movieId = models.IntegerField()
    imdbId = models.IntegerField()
    tmdbId = models.IntegerField()

    class Meta:
        ordering = ['movieId']

    def __str__(self):
        return f'{self.movieId}'

class Recommendations(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.CharField(max_length=200)
    recommendation_model = models.CharField(max_length=200, default="NaN")

    def movies_default():
        return {"movies":["a","b","c"]}

    movies = models.ManyToManyField(MoviesRanked)

    user_description_short = models.CharField(default='', max_length=500)
    user_description_long = models.CharField(default='', max_length=1000)


    def __str__(self):
        return f'{self.userId} with model {self.recommendation_model}'
    

class UserRankings(models.Model):
    userId = models.CharField(max_length=200)
    movieId = models.IntegerField()
    rank = models.IntegerField()

    def __str__(self):
        return f'{self.userId} on movie {self.movieId}'

class FinalResult(models.Model):
    userId = models.CharField(max_length=200)
    answers = models.JSONField()
