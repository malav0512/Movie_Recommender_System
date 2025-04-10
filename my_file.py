import streamlit as st
import pickle
import pandas as pd
import requests
import socket
from requests.packages.urllib3.util import connection

def force_requests_ipv4():
    connection.allowed_gai_family = lambda: socket.AF_INET

force_requests_ipv4()

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommender System')
selected_movie_name=st.selectbox('How would you like to contacted?',movies['title'].values)

def fetch_poster(movie_id):
 try:
  url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=70fd36ce425266e692106ea53385b3a9&language=en-US"
  print(f"Fetching poster for ID {movie_id} with URL: {url}")
  response = requests.get(url, timeout=10)  # Reduce timeout for responsiveness
  response.raise_for_status()  # Raises HTTPError if not 200 OK

  data = response.json()
  poster_path = data.get('poster_path')
  print("Poster path:", poster_path)

  if poster_path:
    full_path = "https://image.tmdb.org/t/p/w500" + poster_path
  else:
            # Fallback image if poster_path not available
    full_path = "https://via.placeholder.com/500x750.png?text=No+Image"

    return full_path

 except requests.exceptions.RequestException as e:
  print(f"Error fetching poster for movie_id={movie_id}: {e}")
  return "https://via.placeholder.com/500x750.png?text=No+Image"

def recommend(movie):
 movie_index=movies[movies['title']==movie].index[0]
 distances=similarity[movie_index]
 movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
 recommended_movies=[]
 recommended_movies_posters=[]
 #fetch poster from api

 print("Recommended movie IDs:")  # Debug print
 for i in movies_list:
  movie_id=movies.iloc[i[0]].movie_id
  print(movie_id)
  recommended_movies.append(movies.iloc[i[0]].title)
  recommended_movies_posters.append(fetch_poster(movie_id))
 return recommended_movies,recommended_movies_posters

if st.button('Recommend'):
 names,posters=recommend(selected_movie_name)

 col1, col2, col3, col4, col5= st.columns(5)

 with col1:
  st.text(names[0])
  st.image(posters[0])
 with col2:
  st.text(names[1])
  st.image(posters[1])
 with col3:
  st.text(names[2])
  st.image(posters[2])
 with col4:
  st.text(names[3])
  st.image(posters[3])
 with col5:
  st.text(names[4])
  st.image(posters[4])
