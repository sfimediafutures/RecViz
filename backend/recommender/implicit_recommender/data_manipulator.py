import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from pandas.api.types import CategoricalDtype


def load_data():
	# read Movielens csv or get it somewhere
	data = pd.read_csv('ratings.csv')
	#data[userId  movieId  rating  timestamp]
	#remove the timestamp column
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
		temp = {"userId": user, "movieId": int(movie), "rating": 5.0}
		rows_to_add.append(temp)

	rows_to_add = pd.DataFrame(rows_to_add)
	original_data = original_data.append(rows_to_add, ignore_index=True)
	return original_data


def make_sparse(data):
	# convert the data to sparse matrices

	# is there a more elegant way to map this? it maps user and movie IDs to integer labels like (1, 5, 27, 4, 5) -> (0, 1, 2, 3,)
	users_list = data["userId"].unique()
	users_map = {}
	i = 0
	for user in users_list:
		users_map[user] = i
		i+=1

	movies_list = data["movieId"].unique()
	movies_map = {}
	i = 0
	for movie in movies_list:
		movies_map[movie] = i
		i += 1

	data_ = data
	data_["userId"] = data_["userId"].map(users_map)
	data_["movieId"] = data_["movieId"].map(movies_map)
	users_col = data_["userId"].tolist()
	movies_col = data_["movieId"].tolist()
	shape = (len(users_list), len(movies_list))
	print(shape)
	print(max(users_col), max(movies_col))

	user_item_coo = coo_matrix((np.array(data["rating"].tolist()), (np.array(users_col), np.array(movies_col))), shape=shape)
	user_item = user_item_coo.tocsr()
	print(user_item)

	return user_item, users_map, movies_map
