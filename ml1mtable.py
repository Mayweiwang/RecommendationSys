__author__ = 'wangwei'

import pandas as pd

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('./ml-1m/users.dat',
                      sep='::', header=None, names=unames, engine='python')

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('./ml-1m/ratings.dat',
                        sep='::', header=None, names=rnames, engine='python')

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('./ml-1m/movies.dat',
                       sep='::', header=None, names=mnames, engine='python')

# combine three tables together
movielens = pd.merge(pd.merge(ratings, users), movies)

# try to create a table with (user, title) matrix
usersprefs = movielens.pivot_table('rating', index='user_id', columns='title')

df = pd.DataFrame(usersprefs)
df2 = df.reset_index().rename(columns={'index':'user_id'})
df3 = pd.melt(df2,'user_id',var_name='title').dropna()
df4 = df3.reset_index(drop=True)
# df5 = df3[['title', 'user_id', 'value']].reset_index(drop=True)

def createprefs(df4):
    critics1 = {k: g['title'].tolist() for k, g in df4.groupby('user_id')}
    critics2 = {k: g['value'].tolist() for k, g in df4.groupby('user_id')}
    return critics1, critics2

def createprefs2(df4):
    critics3 = {k: g['user_id'].tolist() for k, g in df4.groupby('title')}
    critics4 = {k: g['value'].tolist() for k, g in df4.groupby('title')}
    return critics3, critics4
# group by title
ratings_by_title = movielens.groupby('title').size()



