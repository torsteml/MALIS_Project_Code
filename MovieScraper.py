#!/usr/bin/env python
# coding: utf-8

# In[198]:


import seaborn as sns
import numpy as np
import pandas as pd


# In[209]:


movies_dataframe = pd.read_csv('../dataset/movie_titles.txt', usecols=range(3), encoding='latin1', header=None) #Movie title may contain comma.
movies_dataframe.columns = ['MovieID','YearOfRelease','Title']
#movies_dataframe = movies_dataframe[:10]
movies_dataframe


# In[227]:


import requests
#returns the internal ID for use towards the Movie DB api. If no movie found, returns -1
def getTheMovieDbId(title, year):
    url = "https://api.themoviedb.org/3/search/movie"
    api_key = "936803e93cf0f57238bc692f7cfed8d6"
    api_key = "936803e93cf0f57238bc692f7cfed8d6"
    payload = {"api_key":api_key, "language":"en-US", "query":title, "include_adult":"false", "year":year}
    r = requests.get(url, params=payload)
    data = r.json()
    choise = 0
    try: 
        return data['results'][choise]['id']
    except:
        return -1
    
def getMovieInformation(tmdbID):
    url = "https://api.themoviedb.org/3/movie/" + str(tmdbID)
    api_key = "936803e93cf0f57238bc692f7cfed8d6"
    payload = {"api_key":api_key, "language":"en-US"}
    r = requests.get(url, params=payload)
    data = r.json()
    return data


# In[204]:


movies_dataframe['Budget'] = 0
movies_dataframe['Genre'] = ''
movies_dataframe['Original_language'] = ''
movies_dataframe['Runtime'] = 0
for i in range(len(movies_dataframe)):
    title = movies_dataframe.at[i,'Title']
    year = movies_dataframe.at[i,'YearOfRelease']
    tmdbID = getTheMovieDbId(title, year)
    if(tmdbID != -1):
        moviedata = getMovieInformation(tmdbID)
        print("Appended ", title, ' as ', moviedata['title'])
        if(len(moviedata)>0):
            movies_dataframe.at[i,'Budget'] = moviedata['budget']
            movies_dataframe.at[i,'Original_language'] = moviedata['original_language']
            movies_dataframe.at[i,'Runtime'] = moviedata['runtime']
        if(len(moviedata['genres'])>0):
            movies_dataframe.at[i,'Genre'] = moviedata['genres'][0]['name']
    else:
        print("Failed to append: ", title)
    print(i+1,"/",len(movies_dataframe)," (", (i+1)/len(movies_dataframe), ")")
    
movies_dataframe[:10]

movies_dataframe.to_csv('../dataset/movies_with_features.csv', encoding='utf-8')


# In[221]:


movies_dataframe.loc[movies_dataframe['Title'] == 'The Road to Love']


# In[222]:


movies_dataframe.at[4014,'YearOfRelease']


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




