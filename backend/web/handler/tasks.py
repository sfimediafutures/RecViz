from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from recommender.surprise_recommender import svd_recommender
from recommender import als_recommender
from .models import Recommendations, Movies

@shared_task(bind=True)
def run_recommendations(self, userId, data, model = None):

    # Incoming Data:
    # {"userID": userID, "movies": [movieID, movieID, movieID...]}


    # ==================== ALS ==========================
    #Recommender = als_recommender.ALSRecommender()
    #userId = int(userId)
    #Recommender.run_recommender(user_data=data, user_id=userId)
    #data = Recommender.recs
    #model = 'ALS'

    # ==================== SVD ==========================
    Recommender = svd_recommender.SVDRecommender(20)
    userId = int(userId) # critical for SVD to work
    Recommender.run_recommender(user_id=userId, user_data=data, rerank=True)

    # Access data
    data = Recommender.recs
    #reranked_data = Recommender.reranked_data
    reranked_data = None
    model = 'SVD'
    print(data)
    
    # ==================== --- ==========================
    # Delete any previous recommendation made with ALS that is not a rerank
     # rerank to be added later
    try:
        prev_rec = Recommendations.objects.get(userId = userId, recommendation_model='SVD')
        prev_rec.delete()
    except:
        pass


    # Find new, if there are two for some reason, pick one of them.
    # this filter()[:1].get() step is to avoid edge cases where the user went back and called 
    # the model twice. This also happends in the view and it always picks [:1]
    recommendation = Recommendations.objects.filter(userId = userId, recommendation_model='NaN')[:1].get()

    for objec in data.items():
        for obj in objec[1]:
            recommendation.movies.add(Movies.objects.get(movieId = obj[0]))
    
    recommendation.recommendation_model = 'SVD'
    recommendation.save()


    # Reranked data paresd
    if reranked_data:
        recommendation = Recommendations(userId = userId)
        recommendation.save()
        recommendation.recommendation_model = 'SVD-reranked'
    
        for objec in reranked_data.items():
            for obj in objec[1]:
                recommendation.movies.add(Movies.objects.get(movieId = obj[0]))

        recommendation.save()