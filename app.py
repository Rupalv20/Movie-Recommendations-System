import pickle
import requests
import streamlit as st
import pandas as pd
import numpy as np
# we need to import a new library named as request to fetch api from tmdb.

# creating a variable named as movies_dict and load the movies_dict.pkl file in it in the read binary format.
# creating a dataframe named as movies using the dictionary movies_dict.


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# loading the similarity variable from vsc using pickle
similarity1 = pickle.load(open('similarity1.pkl', 'rb'))
similarity2 = pickle.load(open('similarity2.pkl', 'rb'))
similarity = np.concatenate([similarity1, similarity2])

# this function helps to give you the name of the 5 recommended movies when we are passing the name of a movie.
# just copy and paste the same function from vsc and makes some changes like instead of print use append function.
# fetching posters by using movie id from apk
def fetch_posters(movie_id):
    # get function used to get the api path of the poster
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=dde7361a12136233ac29048cf54ea65e'.format(movie_id))
    # json file is used to show the path of the poster but not the complete path so we need to add tmdb image path as
    # well with the json poster path
    data = response.json()
    # complete poster path:
    return "https://image.tmdb.org/t/p/original" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        # fetching posters using movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_posters(movie_id))
    return recommended_movies, recommended_movies_posters


# to take movies as an input in the selection box
st.title('Movie Recommender System')
# the name of the movie will be fetched using the option ,erase option and write selected movie name.
selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    # putting the names of the movies in the select box dropdown menu by using movies dataframe.
    movies['title'].values
)
# putting a button option in the streamlit app. here we put Recommend as the name of the button and what the button
# will be showing is done by selected_movies_names inside the st.write
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    # print("Length ", len(names))
    # now we need to display the names and posters for that we will go to the streamlit documentation and there we will
    # use the code from the layout your app command under that go to columns section and copy paste the code
    # for 5 movies we need to use 5 columns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        # noinspection PyUnboundLocalVariable
        st.header(names[0])
        # noinspection PyUnboundLocalVariable
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])

    with col4:
        st.header(names[3])
        st.image(posters[3])

    with col5:
        st.header(names[4])
        st.image(posters[4])
