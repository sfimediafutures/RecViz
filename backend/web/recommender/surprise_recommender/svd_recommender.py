from .data_manipulator import *
from surprise import SVD
from collections import defaultdict
from timeit import default_timer as timer

from ..cp_reranker import *


def get_top_n(predictions, n=10):
	"""Return the top-N recommendation for each user from a set of predictions.

	Args:
		predictions(list of Prediction objects): The list of predictions, as
			returned by the test method of an algorithm.
		n(int): The number of recommendation to output for each user. Default
			is 10.

	Returns:
	A dict where keys are user (raw) ids and values are lists of tuples:
		[(raw item id, rating estimation), ...] of size n.
	"""

	# First map the predictions to each user.
	top_n = defaultdict(list)
	for uid, iid, true_r, est, _ in predictions:
		top_n[uid].append((iid, est))

	# Then sort the predictions for each user and retrieve the k highest ones.
	for uid, user_ratings in top_n.items():
		user_ratings.sort(key=lambda x: x[1], reverse=True)
		top_n[uid] = user_ratings[:n]

	return top_n

class SVDRecommender:

	def __init__(self, k):
		self.pandas_data = None
		self.surprise_data = None
		self.recs = None
		self.model = SVD()
		self.K = k

	def get_recs(self, user_id):
		items = self.pandas_data['movieId'].unique()

		predicts = []
		for item_id in items:
			predicts.append(self.model.predict(user_id, item_id))

		res = get_top_n(predicts, n=self.K)
		return res

	def run_recommender(self, user_id=None, user_data=None, rerank=False):
		self.pandas_data = load_data()
		self.pandas_data = add_test_user(user_data, self.pandas_data)
		print(self.pandas_data.tail(30))
		self.surprise_data = prepare_data(self.pandas_data)

		print("Training the model...")
		start = timer()
		self.model.fit(self.surprise_data)
		end = timer()
		print("Training took:", end - start)


		print("Generating recommendations...")
		print(('userid',user_id))
		if not rerank:
			self.recs = self.get_recs(user_id=user_id)

			print(self.recs)
			# TODO: fix the output format
			# so far it returns stuff like this:
			# defaultdict(<class 'list'>, {1: [(2905, 4.85019300448541), (260, 4.831475413112318),...
		else:
			
			old_k = self.K
			self.K = 200
			big_recs = self.get_recs(user_id=user_id)
			print("Starting reranking the recommendations")
			cp = CP(k=old_k)
			res = cp.run(user_id, big_recs, self.pandas_data)
			print(res)
			self.recs = res

		return

