
# model
import pandas as pd
from libreco.algorithms import UserCF
from libreco.data import DatasetPure
from libreco.data import split_by_ratio_chrono, DatasetPure

# serving
from libreco.utils import save_knn
from serving.flask import sim2redis, user_consumed2redis


# removing unnecesarry tensorflow logging
import os
import tensorflow as tf
from torch import save
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["KMP_WARNINGS"] = "FALSE"
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


data = '../data/ml-latest-small/'
path = 'knn_model'
if __name__ == "__main__":
    # import data
    data = pd.read_csv(data + 'ratings.csv',
                        names=["user", "item", "label", "time"],
                        skiprows=1)

    # prepare data
    train_data, eval_data = split_by_ratio_chrono(data, test_size=0.2)
    train_data, data_info = DatasetPure.build_trainset(train_data)
    eval_data = DatasetPure.build_evalset(eval_data)
    
    # create model
    user_cf = UserCF(task="rating", data_info=data_info, k=20, sim_type="cosine")
    user_cf.fit(train_data, verbose=2, mode="invert", num_threads=4, min_common=1,
                eval_data=eval_data, metrics=["rmse", "mae", "r2"])

    user_cf.recommend_user(user=2000000, n_rec=10, cold_start='popular')
    # store model to redis
    save_knn(path, user_cf, train_data=train_data, k=20)
    sim2redis(path)
    user_consumed2redis(path)

    