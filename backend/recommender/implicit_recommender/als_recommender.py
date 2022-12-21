from implicit.als import AlternatingLeastSquares
from implicit.evaluation import *
from data_manipulator import *
from implicit.nearest_neighbours import bm25_weight


class ALSRecommender:

	def __init__(self, f=35, it=20, r=0.01, k=50):
		# initialize the parameters for the ALS recommender:
		# f - number of factors; it - iterations; r - regularization parameter
		# check https://github.com/benfred/implicit for details on ALS implementation
		self.data = None
		self.sparse_item_user = None
		self.recs = None
		# maps used to translate matrix indices to user and item IDs
		self.user_map = None
		self.item_map = None

		self.model = AlternatingLeastSquares(factors=f, regularization=r, iterations=it, calculate_training_loss=True)
		self.K = k

	def train(self, item_user_data):
		# TODO: these three lines are ONLY FOR TESTING, remove later
		# ============================
		train, test = train_test_split(item_user_data, train_percentage=0.8)
		self.model.fit(train)
		print(ranking_metrics_at_k(self.model, train.T.tocsr(), test.T.tocsr(), K=10, num_threads=4, show_progress=False))
		# ============================

		print("Training the model...")
		self.model.fit(item_user_data)
		print("Finished!")

	def get_recs(self, user_id, k):
		recommendations = self.model.recommend(self.user_map(user_id), self.sparse_item_user, N=k)
		recommendations_data = []
		reverse_item_map = {v: k for k, v in self.item_map.items()}
		for pair in recommendations:
			d = {"userId": user_id, "itemId": reverse_item_map[pair[0]], "score": pair[1]}
			recommendations_data.append(d)
		print(recommendations_data)
		return recommendations_data

	def run_recommender(self, user_id, rerank=False):
		#train a model and get recommendation list of length K for a user with user_id
		# load the Movielens data here, add the test user data and convert to sparse matrices for Implicit
		self.data = load_data()

		#TODO: fix this later for adding the test user data
		#user_data = None
		#ratings_data = add_test_user(ratings_data, user_data)
		self.sparse_item_user, self.user_map, self.item_map = make_sparse(self.data)

		self.sparse_item_user = bm25_weight(self.sparse_item_user, K1=3, B=1).tocsr()

		# train the ALS model
		self.train(self.sparse_item_user)
		# and generate recommendation in a list [{"userId": user_id, "itemId": itemid, "score": score}, ...]
		# if reranker set to false then just recommend short list,
		# otherwise generate CP instance to rerank a long recommendation list
		if not rerank:
			self.recs = self.get_recs(user_id, self.K)
		else:
			long_recs = self.get_recs(user_id, 150)
			# TODO: add here the reranker implementation, to be tested
			'''cp = CP()
			self.recs = cp.run(user_id, long_recs, self.data)'''

		return
