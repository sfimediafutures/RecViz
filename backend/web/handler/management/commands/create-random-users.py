from django.core.management.base import BaseCommand, CommandError
from handler.models import Movies, UserRankings, Submission, Recommendations
import random
class Command(BaseCommand):
    help = 'Creates n random users, default is 10 and gives n ratings, default is 30'

    # internal function to grab random user ID's 
    def __random_userid(self, n):
        for i in range(n):
            yield random.randint(10000, 99999)

    # Adding avg ratings
    def __create_ratings_from_avg(self, n):
        return True

    def add_arguments(self, parser):
        parser.add_argument('--n_users', 
                            type=int,
                            action='store',
                            help='How many users to be created',
                            default=10,
                            dest='n_users'
                            )

        parser.add_argument('--n_ratings', 
                            type=int,
                            action='store',
                            help='How many ratings each user gives',
                            default=30,
                            dest='n_ratings'
                            )

        parser.add_argument('--train', 
                            type=bool,
                            action='store',
                            help='If you should train on these submissions, default is True',
                            default=True,
                            dest='train'
                            )
        
        parser.add_argument('--rating', 
                            type=int,
                            action='store',
                            help='What rating is given to the movies, default is 5',
                            default=5,
                            dest='rating'
                            )




    def handle(self, *args, **options):
        for user in self.__random_userid(options['n_users']):
            # Get movies
            try:
                # Best way to get random objects that im aware of
                n = Movies.objects.values_list('movieId',flat = True)
                # k = n movies, so 30 movies
                if n.count() < 30:
                    raise CommandError('No or too few movies in Model, "%s" movies exist.' % n.count())
                # Movie.object.get(movieId == Anastasiia-smovieid)
                else: movies = random.choices(n, k=options['n_ratings'])

            except Movies.DoesNotExist:
                raise CommandError('No movies')

                # Create Ratings
            for movieId in movies:
                UserRankings.objects.create(userId = str(user), movieId = movieId, rank=options['rating'])

            # Create Submissions
            Submission.objects.create(userId = str(user),answers = {}, pageId='Added by Admin', train_on_submission=options['train'])

            self.stdout.write(self.style.SUCCESS(f'Successfully added { options["n_users"] } with { options["n_ratings"] } ratings of { options["rating"] }.'))
