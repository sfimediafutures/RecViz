from urllib.request import Request
from rest_framework import serializers
from handler.models import Submission, Genre, Links, Recommendations, UserRankings, MoviesRanked


# Creating serializer class

class SubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    userId = serializers.CharField(max_length=100)
    pageId = serializers.CharField(max_length=100)
    train_on_submission = serializers.BooleanField()
    final_submission = serializers.BooleanField()
    answers = serializers.JSONField()

    def create(self, validated_data):
        return Submission.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.userId = validated_data.get('user_id', instance.user_id)
        instance.answers = validated_data.get('answers', instance.answers)
        return instance

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = ['movieId','imdbId','tmdbId']

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    movieId = serializers.IntegerField()
    title = serializers.CharField()
    genre = GenreSerializer(many=True)
    links = LinksSerializer(many=True)

class MovieRankedSerializer(serializers.Serializer):
    tmdbId = serializers.IntegerField()
    rank = serializers.IntegerField()
    cached_img_url = serializers.CharField()
    cached_background_img_url = serializers.CharField()
    movie = MovieSerializer()


class ImageSerializerField(serializers.Field):
    def to_representation(self, values):
        return values['']
    def to_internal_value(self, data):
        return

class MovieSerializerImage(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    movieId = serializers.IntegerField()
    title = serializers.CharField()
    genre = GenreSerializer(many=True)
    links = LinksSerializer(many=True)

    def get_image(self, obj):
        title = 'beep bop'
        return obj.title

class RecommendationSerializer(serializers.Serializer):
    userId = serializers.CharField()
    recommendation_model = serializers.CharField()
    movies = MovieRankedSerializer(many=True)

class UserRankingsSerializer(serializers.Serializer):
    userId = serializers.CharField()
    movieId = serializers.IntegerField()
    rank = serializers.IntegerField()

    def create(self, validated_data):
        return UserRankings.objects.create(**validated_data)

# For any other classes that needs serializing, the same can be achieved with ModelSerilaizer class, 
# see https://www.django-rest-framework.org/tutorial/1-serialization/#using-modelserializers
# I have simply chosen to use the manual method due to our JSONField(). 
