#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import datetime
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity


# In[3]:


genome_scores_data = pd.read_csv('genome-scores.csv') 
movies_data = pd.read_csv('movies.csv') 
ratings_data = pd.read_csv('ratings.csv')


# In[4]:


genome_scores_data.head()


# In[5]:


movies_data.head()


# In[6]:


ratings_data.head()


# In[7]:


scores_pivot = genome_scores_data.pivot_table(index = ["movieId"],columns = ["tagId"],values = "relevance").reset_index()
scores_pivot.head()


# In[8]:


#join
mov_tag_df = movies_data.merge(scores_pivot, left_on='movieId', right_on='movieId', how='left')
mov_tag_df = mov_tag_df.fillna(0) 
mov_tag_df = mov_tag_df.drop(['title','genres'], axis = 1)
mov_tag_df.head()


# In[9]:


def set_genres(genres, col):
    if genres in col.split('|'): return 1
    else: return 0


# In[10]:


mov_genres_df = movies_data.copy()

mov_genres_df["Action"] = mov_genres_df.apply(lambda x: set_genres("Action",x['genres']), axis=1)
mov_genres_df["Adventure"] = mov_genres_df.apply(lambda x: set_genres("Adventure",x['genres']), axis=1)
mov_genres_df["Animation"] = mov_genres_df.apply(lambda x: set_genres("Animation",x['genres']), axis=1)
mov_genres_df["Children"] = mov_genres_df.apply(lambda x: set_genres("Children",x['genres']), axis=1)
mov_genres_df["Comedy"] = mov_genres_df.apply(lambda x: set_genres("Comedy",x['genres']), axis=1)
mov_genres_df["Crime"] = mov_genres_df.apply(lambda x: set_genres("Crime",x['genres']), axis=1)
mov_genres_df["Documentary"] = mov_genres_df.apply(lambda x: set_genres("Documentary",x['genres']), axis=1)
mov_genres_df["Drama"] = mov_genres_df.apply(lambda x: set_genres("Drama",x['genres']), axis=1)
mov_genres_df["Fantasy"] = mov_genres_df.apply(lambda x: set_genres("Fantasy",x['genres']), axis=1)
mov_genres_df["Film-Noir"] = mov_genres_df.apply(lambda x: set_genres("Film-Noir",x['genres']), axis=1)
mov_genres_df["Horror"] = mov_genres_df.apply(lambda x: set_genres("Horror",x['genres']), axis=1)
mov_genres_df["Musical"] = mov_genres_df.apply(lambda x: set_genres("Musical",x['genres']), axis=1)
mov_genres_df["Mystery"] = mov_genres_df.apply(lambda x: set_genres("Mystery",x['genres']), axis=1)
mov_genres_df["Romance"] = mov_genres_df.apply(lambda x: set_genres("Romance",x['genres']), axis=1)
mov_genres_df["Sci-Fi"] = mov_genres_df.apply(lambda x: set_genres("Sci-Fi",x['genres']), axis=1)
mov_genres_df["Thriller"] = mov_genres_df.apply(lambda x: set_genres("Thriller",x['genres']), axis=1)
mov_genres_df["War"] = mov_genres_df.apply(lambda x: set_genres("War",x['genres']), axis=1)
mov_genres_df["Western"] = mov_genres_df.apply(lambda x: set_genres("Western",x['genres']), axis=1)
mov_genres_df["(no genres listed)"] = mov_genres_df.apply(lambda x: set_genres("(no genres listed)",x['genres']), axis=1)


# In[11]:


mov_genres_df.drop(['title','genres'], axis = 1, inplace=True)
mov_genres_df.head()


# In[12]:


def set_year(title):
    year = title.strip()[-5:-1]
    if year.isnumeric() == True: return int(year)
    else: return 1800

#add year field
movies = movies_data.copy()
movies['year'] = movies.apply(lambda x: set_year(x['title']), axis=1)
movies = movies.drop('genres', axis = 1)
movies.head()


# In[13]:


#define function to group years
def set_year_group(year):
    if (year < 1900): return 0
    elif (1900 <= year <= 1975): return 1
    elif (1976 <= year <= 1995): return 2
    elif (1996 <= year <= 2003): return 3
    elif (2004 <= year <= 2009): return 4
    elif (2010 <= year): return 5
    else: return 0
movies['year_group'] = movies.apply(lambda x: set_year_group(x['year']), axis=1)
#no need title and year fields
movies.drop(['title','year'], axis = 1, inplace=True)


# In[14]:


agg_movies_rat = ratings_data.groupby(['movieId']).agg({'rating': [np.size, np.mean]}).reset_index()
agg_movies_rat.columns = ['movieId','rating_counts', 'rating_mean']
agg_movies_rat.head()


# In[15]:


#define function to group rating counts
def set_rating_group(rating_counts):
    if (rating_counts <= 1): return 0
    elif (2 <= rating_counts <= 10): return 1
    elif (11 <= rating_counts <= 100): return 2
    elif (101 <= rating_counts <= 1000): return 3
    elif (1001 <= rating_counts <= 5000): return 4
    elif (5001 <= rating_counts): return 5
    else: return 0
agg_movies_rat['rating_group'] = agg_movies_rat.apply(lambda x: set_rating_group(x['rating_counts']), axis=1)
#no need rating_counts field
agg_movies_rat.drop('rating_counts', axis = 1, inplace=True)
mov_rating_df = movies.merge(agg_movies_rat, left_on='movieId', right_on='movieId', how='left')
mov_rating_df = mov_rating_df.fillna(0)
mov_rating_df.head()


# In[16]:


mov_tag_df = mov_tag_df.set_index('movieId')
mov_genres_df = mov_genres_df.set_index('movieId')
mov_rating_df = mov_rating_df.set_index('movieId')


# In[17]:


#cosine similarity for mov_tag_df
cos_tag = cosine_similarity(mov_tag_df.values)*0.5


# In[18]:


#cosine similarity for mov_genres_df
cos_genres = cosine_similarity(mov_genres_df.values)*0.25
#cosine similarity for mov_rating_df
cos_rating = cosine_similarity(mov_rating_df.values)*0.25
#mix
cos = cos_tag+cos_genres+cos_rating


# In[19]:


cos


# In[20]:


cols = mov_tag_df.index.values
inx = mov_tag_df.index
movies_sim = pd.DataFrame(cos, columns=cols, index=inx)
movies_sim.head()


# In[21]:


def get_similar(movieId):
    df = movies_sim.loc[movies_sim.index == movieId].reset_index().             melt(id_vars='movieId', var_name='sim_moveId', value_name='relevance').             sort_values('relevance', axis=0, ascending=False)[1:6]
    return df
#create empty df
movies_similarity = pd.DataFrame(columns=['movieId','sim_moveId','relevance'])


# In[22]:


for x in movies_sim.index.tolist():
    movies_similarity = movies_similarity.append(get_similar(x))
movies_similarity.head()


# In[23]:


def movie_recommender(movieId):
    df = movies_sim.loc[movies_sim.index == movieId].reset_index().             melt(id_vars='movieId', var_name='sim_moveId', value_name='relevance').             sort_values('relevance', axis=0, ascending=False)[1:6]
    df['sim_moveId'] = df['sim_moveId'].astype(int)
    sim_df = movies_data.merge(df, left_on='movieId', right_on='sim_moveId', how='inner').                 sort_values('relevance', axis=0, ascending=False).                 loc[: , ['movieId_y','title','genres']].                 rename(columns={ 'movieId_y': "movieId" })
    return sim_df


# In[24]:


#get recommendation for Toy Story
movie_recommender(1)


# In[25]:


#get recommendation for Inception
movie_recommender(79132)


# In[26]:


users_df = pd.DataFrame(ratings_data['userId'].unique(), columns=['userId'])
users_df.head()


# In[27]:


#create movies_df
movies_df = movies_data.drop('genres', axis = 1)
#calculate mean of ratings for each movies
agg_rating_avg = ratings_data.groupby(['movieId']).agg({'rating': np.mean}).reset_index()
agg_rating_avg.columns = ['movieId', 'rating_mean']
#merge
movies_df = movies_df.merge(agg_rating_avg, left_on='movieId', right_on='movieId', how='left')
movies_df.head()


# In[28]:


genres = [
    "Action",
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western",
    "(no genres listed)"]
genres_df = pd.DataFrame(genres, columns=['genres'])
genres_df.head()


# In[29]:


users_movies_df = ratings_data.drop('timestamp', axis = 1)
users_movies_df.head()


# In[30]:


movies_genres_df = movies_data.drop('title', axis = 1)


# In[31]:


#define a function to split genres field
def get_movie_genres(movieId):
    movie = movies_genres_df[movies_genres_df['movieId']==movieId]
    genres = movie['genres'].tolist()
    df = pd.DataFrame([b for a in [i.split('|') for i in genres] for b in a], columns=['genres'])
    df.insert(loc=0, column='movieId', value=movieId)
    return df


# In[32]:


#create empty df
movies_genres=pd.DataFrame(columns=['movieId','genres'])
for x in movies_genres_df['movieId'].tolist():
    movies_genres=movies_genres.append(get_movie_genres(x))
movies_genres.head()


# In[33]:


#join to movies data to get genre information
user_genres_df = ratings_data.merge(movies_data, left_on='movieId', right_on='movieId', how='left')
#drop columns that will not be used
user_genres_df.drop(['movieId','rating','timestamp','title'], axis = 1, inplace=True)
user_genres_df.head()


# In[34]:


def get_favorite_genre(userId):
    user = user_genres_df[user_genres_df['userId']==userId]
    genres = user['genres'].tolist()
    movie_list = [b for a in [i.split('|') for i in genres] for b in a]
    counter = Counter(movie_list)
    return counter.most_common(1)[0][0]


# In[41]:


#create empty df
users_genres = pd.DataFrame(columns=['userId','genre'])
for x in users_df['userId'].tolist():
    print(x)
    users_genres = users_genres.append(pd.DataFrame([[x,get_favorite_genre(x)]], columns=['userId','genre']))
users_genres.head()




