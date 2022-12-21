from sys import stdout
from handler.models import Movies, Genre, Links

def run():
    # Fetch all questions
    movies = Movies.objects.all()
    # Delete questions
    movies.delete()

        # Fetch all questions
    genres = Genre.objects.all()
    # Delete questions
    genres.delete()

        # Fetch all questions
    links = Links.objects.all()
    # Delete questions
    links.delete()