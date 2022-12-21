import operator

from scipy.spatial.distance import jensenshannon

'''==================================================
Find the cutoff point between item categories defined by the popularity percentage 
from a list of items sorted by popularity
=================================================='''
def find_short_head_split_point(sorted_list, percentage):
	s = 0.0
	eightyPercent = float(sum(sorted_list)) * percentage
	for i in range(len(sorted_list)):
		s += sorted_list[i]
		if s >= eightyPercent:
			return i


class CP:

	def __init__(self, alpha=0.9, k=150, head_percentage=0.2):
		self.alpha = alpha
		self.k = k
		self.head_percentage = head_percentage
		self.tail_percentage = 1 - head_percentage
		self.G = None

	def run(self, user, recs, rating_data):
		data = rating_data
		users = data.userId.unique()
		items = data.movieId.unique()
		print("Users total:" + str(len(users)) + "\nItems total:" + str(len(items)))
		item_pops = data.groupby('movieId').size() / len(users)

		item_pops_total = data.groupby('movieId').size()

		sorted_item_pops_map = sorted(item_pops_total.items(), reverse=True, key=operator.itemgetter(1))
		sorted_items = [x[0] for x in sorted_item_pops_map]
		sorted_ratio = [x[1] for x in sorted_item_pops_map]

		short_head_point = find_short_head_split_point(sorted(item_pops, reverse=True), self.head_percentage)
		mid_tail_point = find_short_head_split_point(sorted(item_pops, reverse=True), self.tail_percentage)
		indexes = [short_head_point, mid_tail_point, len(item_pops)]

		# list of three item groups: head, mid, tail
		s = 0
		for i in range(len(indexes)):
			self.G.append([x[0] for x in sorted_item_pops_map[s:int(indexes[i])]])
			s = int(indexes[i])

		reranked = self.calib_rec(user, recs, data)

		return reranked

	'''==================================================
		Calculates the score for a recommendation list based on the relevancy 
		and deviation from the user preference
		recom: list of the recommended items for the user
		rated: list of items in user history
		rating dict: ratings of the items in user history
		alpha: regularization term for CP, weighs the importance of relevancy and deviation differently
		=================================================='''
	def cp(self, recom, rated, rating_dict):
		dist = [len(set(self.G[0]).intersection(set(recom))), len(set(self.G[1]).intersection(set(recom))),
				len(set(self.G[2]).intersection(set(recom)))]
		dist = [float(x) / self.k for x in dist]

		relevance_sum = 0
		for i in recom:
			rating = rating_dict[i]
			relevance_sum += rating

		left = (1 - self.alpha) * relevance_sum
		j = jensenshannon(rated, dist)
		right = self.alpha * j
		res = left - right
		return res

	'''==================================================
		CP rerank the recommendation lists 
		takes recs as long ALS recommendation lists, alpha is regularization for CP 
		and k is the desired new reranked recommendation list length (MUST BE SMALLER THAN LENGTH IN RECS)
		the sorting algorithm is based on www.sciencedirect.com/science/article/pii/S0957417417302075
		=================================================='''
	def calib_rec(self, user, recs, rating_data):
		print("Calibrating for the user " + str(user))
		reranked = []

		user_recs = recs.loc[recs['user'] == user]
		items = user_recs['item'].unique()
		rating_dict = {}
		for index, row in user_recs.iterrows():
			rating_dict[row['item']] = row["rating"]

		# original user probabilities
		UG1 = []
		UG2 = []
		UG3 = []
		history = rating_data[rating_data.user == user]['item']

		# print("User history:", len(history))
		for i in history:
			if i in self.G[0]:
				UG1.append(i)
			elif i in self.G[1]:
				UG2.append(i)
			else:
				UG3.append(i)
		ug = [len(UG1), len(UG2), len(UG3)]
		s = sum(ug)
		rated = [float(x) / s for x in ug]

		T = items[:self.k]
		X = items[self.k:]

		old_list = items[:self.k]
		new_list = items[:self.k]
		for i in X:
			delta = 0
			new_list = old_list.copy()
			init_cp = self.cp(old_list, rated, rating_dict)
			for index in range(1, self.k + 1):
				new_list[-index] = i
				new_cp = self.cp(new_list, rated, rating_dict)
				if new_cp - init_cp > delta:
					old_list = new_list.copy()
					delta = new_cp - init_cp

		for item in old_list:
			score = user_recs.loc[user_recs['item'] == item, 'rating'].item()
			d = {'item': item, 'rating': score}
			reranked.append(d)

		return reranked
