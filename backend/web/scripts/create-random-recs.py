from sys import stdout
from handler.models import Movies, Genre, Links, Recommendations, UserRankings, Submission
import random
from django.core.exceptions import ObjectDoesNotExist
def run():
    # Fetch all questions
    def random_userid(n):
        for i in range(n):
            yield random.randint(10000, 99999)
        
    # 10 users:
    for i in random_userid(10):
        n = Movies.objects.values_list('movieId',flat = True)
        # k = n movies, so 30 movies
        movies = random.choices(n, k=30)
        print(movies)
        # ratings:
        for movieId in movies:
            # rank = rating
            UserRankings.objects.create(userId = str(i), movieId = movieId, rank=5)

        Submission.objects.create(userId = str(i),answers = {}, pageId='Added by Admin', train_on_submission=True)

        #answers:{},
		#			train_on_submission : train,
		#			final_submission : final,
        #           userId : uId,
        #			pageId : document.title
	    #}

    #userId = models.CharField(max_length=200)
    #movieId = models.IntegerField()
    #rank = models.IntegerField()




    
