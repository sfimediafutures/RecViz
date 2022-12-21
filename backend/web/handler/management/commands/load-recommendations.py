from django.core.management.base import BaseCommand, CommandError
from handler.models import Movies, UserRankings, Submission, Recommendations, MoviesRanked
import json


class Command(BaseCommand):
    help = 'Loads users.json from /data/recommendations/users.json'

    # internal function to grab random user ID's 
    def add_arguments(self, parser):
        parser.add_argument('file',
                            type=str,
                            action='store',
                            help='What file should be loaded',
                            )

        parser.add_argument('--root-data-folder',
                            type=str,
                            action='store',
                            help='If using a different root folder other than /data/recommendations/',
                            default='/data/recommendations',
                            dest='root_data_folder'
                            )

    def handle(self, *args, **options):
        try:
            with open(options['root_data_folder'] + '/' + options['file']) as f:
                data = json.load(f)
        except Exception as e:
            print(e)
        # try:
        for item in data:
            for recommender in item['recommendations'].keys():
                userId = item['userId']
                recommendation_model = recommender
                user_description_short = item['user_description_short']
                user_description_long = item['user_description_long']
                recommendation = Recommendations.objects.create(userId=userId,
                                                                recommendation_model=recommendation_model,
                                                                user_description_short=user_description_short,
                                                                user_description_long=user_description_long)

                movies = list(item['recommendations'][recommender].values())
                for movie in movies[0][:20]:
                    # try:
                        # CHANGE ME! Get tmdbid based on movieID, create a new object in new model MovieRanked, add MovieRanked value to recommender model.
                        #movie = [moveId, tmdbID, rank]
                        # Create new ranked movies]
                    print(movie)
                    mov = Movies.objects.get(movieId=movie[0])
                    print(mov)
                    
                    tmdbId = mov.links()[0].tmdbId
                    print(tmdbId)
                    new_movie = MoviesRanked(movie = mov, tmdbId = tmdbId, rank = movie[1])
                    new_movie.save()
                    print(new_movie)
                    recommendation.movies.add(new_movie) # add rank for movie in recommender model
                    # except Movies.DoesNotExist:
                    #     raise CommandError(f'Movie with movieId {movie} does not exist in database.')
                    recommendation.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully added Recommendation for user {userId} and model {recommendation_model}'))
        # except Exception as e:
        #     print(e)
