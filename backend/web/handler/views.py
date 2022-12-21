from handler.models import ( 
    Submission, Movies, Recommendations, UserRankings
)
from rest_framework import status
from rest_framework.decorators import api_view
from handler.serializers import (
    SubmissionSerializer, MovieSerializer, MovieSerializerImage,
    RecommendationSerializer, UserRankingsSerializer
    )

from rest_framework import generics, pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend


from django.http import HttpResponse, JsonResponse
from django.http import Http404
from urllib.request import urlopen
import random
import json
import requests as rq
import os

TMDB_KEY = os.environ.get('TMDB_KEY')

# Pagination class
class MoviePagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20


class Submissions_list(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class Submissions_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class Movie_detail(generics.RetrieveAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer

class Movie_list(generics.ListAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer

    # set pagination
    pagination_class = MoviePagination

    # for serach
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']

class Movie_random_list(generics.ListAPIView):
    seq = Movies.objects.all()
    if seq: queryset = random.choices(seq, k=5) 
    else: queryset = []
    serializer_class = MovieSerializer  

class Recommendation(APIView):
    def get_object(self, pk, tk):
        # in some edge cases we have several recommendations from users
        # to combat this we simply return one object.
        if tk:
            try:
                return Recommendations.objects.filter(userId=pk, recommendation_model=str(tk))[:1].get()
            except:
                raise Http404
        else:
            try:
                return Recommendations.objects.filter(userId=pk)[:1].get()
            except:
                raise Http404
        

    def get(self, request, pk, format=None, *args, **kwargs):
        # pk = userId
        # tk = recommenderId
        tk = self.kwargs.get('pk_model', None)
        recommendation = self.get_object(pk, tk)

        
        while recommendation.recommendation_model == 'NaN':
            recommendation = self.get_object(pk)
        serializer = RecommendationSerializer(recommendation)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReccomendationSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class Rating(APIView):
    def get_object(self, pk, tk):
        try:
            return UserRankings.objects.get(userId=pk)
        except UserRankings.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        UserRankings = self.get_object(pk)
        serializer = UserRankingsSerializer(UserRankings)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        UserRankings = self.get_object(pk)
        serializer = UserRankingsSerializer(UserRankings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = UserRankingsSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        UserRankings = self.get_object(pk)
        UserRankings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_recommendation(request, userid, format=None):
    userid = userid

    def create_reccommendations(userid):
        return

    def get_recommendations(userid):
        return

    
    return

@api_view(['GET'])
def movie_get_image(request,pk, format=None):
    i = pk
    api_url = f'https://api.themoviedb.org/3/movie/{i}?api_key={TMDB_KEY}'
    response = rq.get(api_url)
    response.json()
    
    return Response(response.json())


@api_view(['GET'])
def movie_random_new(request, format=None):
    n = Movies.objects.values_list('movieId',flat = True)
    pick = random.choices(n, k=5)

    try:
        result = []
        for movie in pick:
            result.append(Movies.objects.get(movieId = movie))
        serializer = MovieSerializer(result, many=True)
        return Response(serializer.data)
    except Movies.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


# Some of the viewmodels i want to do more custom
@api_view(['GET'])
def movie_random(request, format=None):
    n = Movies.objects.values_list('movieId',)
    pick = random.choice(n)
    try:
        result = Movies.objects.get(movieId = pick)
        serializer = MovieSerializer(result)
        return Response(serializer.data)
    except Movies.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def movie_random_image(request, format=None):
    n = Movies.objects.values_list('movieId',flat = True)
    pick = random.choice(n)
    try:
        result = Movies.objects.get(movieId = pick)
        link = 'https://image.tmdb.org/t/p/w500/m9v9m21TZxvnSjppposZcgDNZeG.jpg'
        serializer = MovieSerializerImage(result)

        with urlopen(url='https://api.themoviedb.org/3/movie/343611?api_key='+TMDB_KEY) as response:
            movie_details = response.read()
        
        return Response(serializer.data)

    except Movies.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
