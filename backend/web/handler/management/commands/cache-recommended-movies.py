from django.core.management.base import BaseCommand, CommandError
from handler.models import Recommendations, MoviesRanked
import os
import requests
import random
class Command(BaseCommand):
    help = 'Caches image links for movies that has a rank or has been recommended to a user'



    def add_arguments(self, parser):
        parser.add_argument('--single-user', 
                            type=str,
                            action='store',
                            help='If you only want to get one user',
                            default='',
                            dest='single_user'
                            )
        
        parser.add_argument('--overwrite', 
                            type=bool,
                            action='store',
                            help='If you want to overwrite previously cached images',
                            default=False,
                            dest='overwrite'
                            )
        
        parser.add_argument('--clear-cache', 
                            type=bool,
                            action='store',
                            help='To clear all cached images',
                            default=False,
                            dest='clear-cache'
                            )

    def handle(self, *args, **options):
        if options['clear-cache']:
            ranked_movies = MoviesRanked.objects.all().delete()
        else:
            TMDB_KEY = os.environ.get('TMDB_KEY')
            try:
                ranked_movies = MoviesRanked.objects.all()
                n = len(ranked_movies)
                i = 0
                for ranked_movie in ranked_movies:
                    if ranked_movie.cached_img_url != "not_cached" or options['overwrite']:
                        self.stdout.write(f'{i}/{n} || Movie {ranked_movie.movie.title} already cached.')
                    else:
                        api_url = f'https://api.themoviedb.org/3/movie/{ranked_movie.tmdbId}?api_key={TMDB_KEY}'
                        response = requests.get(api_url)
                        ranked_movie.cached_img_url = response.json()["poster_path"]
                        ranked_movie.save()
                        self.stdout.write(f'{i}/{n} || Movie {ranked_movie.movie.title}, https://image.tmdb.org/t/p/w200/{response.json()["backdrop_path"]}')

                    i += 1
            except Exception as e:
                self.stdout.write('Something went wrong: \n' + e)