from sys import stdout
from handler.models import Movies, Genre, Links

def run():
    # Fetch all questions
    movies = Movies.objects.filter(movieId > 3952).delete()
