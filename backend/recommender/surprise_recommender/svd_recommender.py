from .data_manipulator import *
from surprise import SVD
from collections import defaultdict
from timeit import default_timer as timer
from backend.web.recommender.reranking.cp_reranker import *

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

	def __init__(self, k=50):
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
		#self.pandas_data = add_test_user(user_data, self.pandas_data)
		self.surprise_data = prepare_data(self.pandas_data)

		print("Training the model...")
		start = timer()
		self.model.fit(self.surprise_data)
		end = timer()
		print("Training took:", end - start)

		print("Generating recommendations...")

		if not rerank:
			self.K = 10
			# TODO: adjust userID
			self.recs = self.get_recs(user_id=1)
			print(self.recs)
			# TODO: fix the output format
			# so far it returns stuff like this:
			# defaultdict(<class 'list'>, {1: [(2905, 4.85019300448541), (260, 4.831475413112318),...
		else:
			self.K = 100
			self.recs = self.get_recs(user_id=1)
			cp = CP()
			reranked = cp.run(user=1, recs=self.recs, rating_data=self.pandas_data)

		return

