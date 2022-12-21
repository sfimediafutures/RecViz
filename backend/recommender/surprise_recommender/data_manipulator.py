import pandas as pd
import numpy as np
from surprise import Dataset
from surprise import Reader


def load_data():
	colnames = ['userId', 'movieId', 'rating', 'timestamp']
	#data[userId  movieId  rating  timestamp]
	#remove the timestamp column
	data = pd.read_csv('../../data/ml_1m/ratings.dat', sep="::", names=colnames)
	data = data.drop(columns=['timestamp'])

	print(data.head())
	print(data.dtypes)

	return data

def add_test_user(user_data, original_data):
	# assume the data is received in the format {"userID": userID, "movies": [movieID, movieID, movieID...]}
	# add rows with the data for the test user
	user = user_data["userId"]
	rows_to_add = []
	movies = user_data["movies"]
	for movie in movies:
		temp = {"userId": user, "movieId": int(movie), "rating": 5}
		rows_to_add.append(temp)

	rows_to_add = pd.DataFrame(rows_to_add)
	original_data = original_data.append(rows_to_add, ignore_index=True)
	return original_data


def prepare_data(data):
	# convert the data surprise Dataset type
	# A reader is still needed but only the rating_scale param is requiered.
	reader = Reader(rating_scale=(1, 5))
	data = Dataset.load_from_df(data[['userId', 'movieId', 'rating']], reader)

	data = data.build_full_trainset()

	return data
