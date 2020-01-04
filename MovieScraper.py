import seaborn as sns
import numpy as np
import pandas as pd
from time import sleep
import requests

url = "https://api.themoviedb.org/3/"
api_key = "936803e93cf0f57238bc692f7cfed8d6"

movies_dataframe = pd.read_csv('../dataset/movie_titles.txt', usecols=range(3), encoding='latin1', header=None) #Movie title may contain comma.
movies_dataframe.columns = ['MovieID','YearOfRelease','Title']

#returns the internal ID for use towards the Movie DB api. If no movie found, returns -1
def getTheMovieDbId(title, year):
    payload = {"api_key":api_key, "language":"en-US", "query":title, "include_adult":"false", "year":year}
    r = requests.get(url + 'search/movie', params=payload)
    data = r.json()
    choise = 0
    try:
        if(data['total_results']>1):
            if(data['results'][0]['title'].startswith(title) and data['results'][0]['release_date'][:4] == str(year)):
                choise = 0
            else:
                return -1
    except:
        pass
    try:
        return data['results'][choise]['id']
    except:
        return -1

#Returns the information struct from the API
def getMovieInformation(tmdbID):
    payload = {"api_key":api_key, "language":"en-US"}
    r = requests.get(url + 'movie/' + str(tmdbID), params=payload)
    data = r.json()
    return data

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
    sleep(2) #So we do not get banned from the API

#Storing to CSV
movies_dataframe.to_csv('../dataset/movies_with_features.csv', encoding='utf-8')
