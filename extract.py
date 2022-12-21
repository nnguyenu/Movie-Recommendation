import pandas as pd
import difflib

#Reading items file:
i_cols = ['movie id', 'movie title' ,'release date','video release date', 'IMDb URL', 'unknown', 
        'Action', 'Adventure','Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama',
         'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
items = pd.read_csv('ml-100k/u.item', sep='|', names=i_cols, encoding='latin-1')
n_items = items.shape[0]
#print('Number of items:', n_items)
X0 = items.to_numpy()
movie_name_list = X0[:,1]
imdb_url_list = X0[:,4]
release_date_list = X0[:,2]
movie_id = X0[:,0]

def read_items(name):
    for i in range(n_items):
        i_name = movie_name_list[i][:-6].lower()
        if name.lower() in i_name:
            return (movie_name_list[i],imdb_url_list[i],release_date_list[i],movie_id[i])
    return ("No movie found",None,None,None)

def read_items_id(id):
    for i in range(n_items):
        if id == movie_id[i]:
            return (movie_name_list[i],imdb_url_list[i],release_date_list[i],movie_id[i])