import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse 

class CF(object):
    # Y_data := ['user_id', 'item_id', 'rating']
    def __init__(self, Y_data, k, dist_func = cosine_similarity, user_CF = 1):
        self.user_CF = user_CF # user-user (1) or item-item (0) CF
        self.Y_data = Y_data if user_CF == 1 else Y_data[:, [1, 0, 2]] # if item-item CF, then switch user and item
        self.k = k # number of neighbor selected
        self.dist_func = dist_func
        self.Ybar_data = None
        # number of users and items
        self.n_users = int(np.max(self.Y_data[:, 0])) + 1
        self.n_items = int(np.max(self.Y_data[:, 1])) + 1

    def add(self, new_data):
        """
        Update Y_data matrix when new ratings come. For simplicity, suppose that there is no new user or item.
        """
        self.Y_data = np.concatenate((self.Y_data, new_data), axis = 0)
    
    def normalize_Y(self):
        users = self.Y_data[:, 0] # all users - 1st col of the Y_data
        self.Ybar_data = self.Y_data.copy()
        self.mean = np.zeros((self.n_users,1))
        for user_id in range(self.n_users):
            ids = np.where(users == user_id)[0]     # row indices of rating done by user_id
            item_ids = self.Y_data[ids, 1] # item ids rated by user_id
            ratings = self.Y_data[ids, 2]  # ratings of user_id
            self.mean[user_id] = np.mean(ratings) 
            if np.isnan(self.mean[user_id]):
                self.mean[user_id] = 0 # avoid empty array & nan value
            # normalize
            self.Ybar_data[ids, 2] = ratings - self.mean[user_id]

        # form the rating matrix as a sparse matrix. We store only nonzeros and their locations.
        # coo_matrix((data, (row_ind, col_ind)), [shape=(M, N)])
        self.Ybar = sparse.coo_matrix((self.Ybar_data[:, 2],
            (self.Ybar_data[:, 1], self.Ybar_data[:, 0])), 
            shape = (self.n_items, self.n_users))
        self.Ybar = self.Ybar.tocsr()   # convert to CSR format for indexing

    def similarity(self):
        self.S = self.dist_func(self.Ybar.T, self.Ybar.T)

    def fit(self):
        """
        Normalize data and calculate similarity matrix again (after some few ratings added)
        """
        self.normalize_Y()
        self.similarity() 
        
    def pred(self, u, i, normalized = 1):
        """ 
        predict the rating of user u for item i (normalized)
        """
        if self.user_CF == 0: u, i = i, u # if item-item CF, switch user and item
        ids = np.where(self.Y_data[:, 1] == i)[0] # find all users who rated i
        users_rated_i = self.Y_data[ids, 0]   # find rating of all users who rated i
        sim = self.S[u, users_rated_i] # find similarity btw current user and ids

        # find k most similarity users and the corresponding similarity levels
        a = np.argsort(sim)[-self.k:]  
        nearest_s = sim[a]

        r = self.Ybar[i, users_rated_i[a]] # rating of near neighbors
        predicted_r = (r * nearest_s)/(np.abs(nearest_s).sum() + 1e-8) # add a small number (1e-8) to avoid dividing by 0
        if normalized == 0:
            predicted_r += self.mean[u] 
        return predicted_r

    def recommend(self, u, normalized = 1):
        """
        Determine all items should be recommended for user u (user_CF = 1)
        or all users who might have interest on item u (user_CF = 0)
        The decision is made based on all i such that: self.pred(u, i) > 0. 
        Suppose we are considering items which have not been rated by u yet. 
        """
        ids = np.where(self.Y_data[:, 0] == u)[0] # row indices of ratings done by u
        items_rated_by_u = self.Y_data[ids, 1] 
        recommended_items = []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                rating = self.pred(u, i)
                if rating > 0: 
                    recommended_items.append(i)

        return recommended_items 

    def print_recommendation(self):
        """
        print all items which should be recommended for each user 
        """
        print('Recommendation: ')
        for u in range(self.n_users):
            recommended_items = self.recommend(u)
            if self.user_CF == 1:
                print('Recommend item(s):', recommended_items, 'to user', u)
            else: 
                print('Recommend item', u, 'to user: ', recommended_items)

r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']

ratings_base = pd.read_csv('ml-100k/movies.csv', sep='\t', names=r_cols, encoding='latin-1')
#ratings_test = pd.read_csv('ml-100k/ub.test', sep='\t', names=r_cols, encoding='latin-1')

print(ratings_base.head(10))