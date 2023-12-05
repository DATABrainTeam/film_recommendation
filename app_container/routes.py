from flask import Blueprint
from flask import request
import requests
import json
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from flask import render_template
import pandas as pd
import numpy as np

bp = Blueprint('main', __name__)
data = pd.read_csv('app_container/0film_cinema.csv')
df_films_info = pd.read_csv('app_container/0tous_films.csv')
df_films = pd.read_csv('app_container/MACHINE.csv')

train_list = [col for col in df_films.columns if col not in ['tconst', 'id', 'Unnamed: 0', 'Unnamed: 0.1', 'runtimeMinutes', 'startYear', 'popularity']]
X = df_films[train_list]
#scaler = StandardScaler().fit(X)
#X_scaled = scaler.transform(X_scaled)
distance = NearestNeighbors(n_neighbors=13).fit(X)

@bp.route('/')
def index():
    indexArg = request.args.get('index')
    title_list = np.array(data['id'].to_list())
    np.random.shuffle(title_list)
    affiche = title_list[:5]
    affiche_list = []

    for film in affiche:
        temp_list = []
        temp_list.append(data[data['id']==film]['primaryTitle'].values[0])
        temp_list.append(data[data['id']==film]['poster_path'].values[0])
        temp_list.append(data[data['id']==film]['averageRating'].values[0])
        temp_list.append(data[data['id']==film]['id'].values[0])

        affiche_list.append(temp_list)


    return render_template('index.html', title='Home', datas=affiche_list)

@bp.route('/movie/<movie_id>')
def movie(movie_id):
    movie_data = df_films_info[df_films_info['id'] == int(movie_id)]

    if movie_data.empty:
        # Handle the case where no movie corresponds to the provided ID
        return render_template('error.html', error_message='Movie not found'), 404

    # API

    url_m = "https://api.themoviedb.org/3/movie/" + str(movie_id) +"?language=en-US"

    headers_m = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlODczNmM0ZTQyNjFhMjgyNDQwN2M1YjFkMzE4ODUxMyIsInN1YiI6IjY1MzhkNTVhYzUwYWQyMDBjYTg5NmJjNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.fvUpyEt1nZDcbXS6jgcgO6rXpPJd-TnPqramQdHq0ko"
    }
    response_movie = requests.get(url_m, headers=headers_m)
    data_movie = json.loads( response_movie.text)

   
    movie_info = [
         movie_data['primaryTitle'].values[0],
         movie_data['poster_path'].values[0],
         movie_data['averageRating'].values[0],
         movie_data['startYear'].values[0],
         data_movie['overview']]

    # API

    url = "https://api.themoviedb.org/3/movie/"+ str(movie_id) + "/credits?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlODczNmM0ZTQyNjFhMjgyNDQwN2M1YjFkMzE4ODUxMyIsInN1YiI6IjY1MzhkNTVhYzUwYWQyMDBjYTg5NmJjNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.fvUpyEt1nZDcbXS6jgcgO6rXpPJd-TnPqramQdHq0ko"
    }

    response = requests.get(url, headers=headers)
    data_api = json.loads( response.text)

    actor_list = []   #il y a la liste de 3 acteurs (je peux faire plus, c'est trop facile, comme tu veux), pour chaque acteur il y a liste de son nom et URL de photo

    for actor in  data_api['cast'][:3]:
        list_temp = [actor['name'], actor['profile_path'] ]
        actor_list.append(list_temp)

    crew_list = [] #juste la liste de directeurs qui ont fait le film
    for crew in data_api['crew']:
        if (crew['known_for_department'] == 'Directing') and (crew['name'] not in crew_list):
            crew_list.append(crew['name'])

    
    # START MACHINE LEARNING
    NNfilm_list = distance.kneighbors([df_films[train_list][df_films['id']==int(movie_id)].values[0]])[1][0]

    film_id = []
    for location in NNfilm_list:
        film_id.append(df_films.loc[location]['id'])

    #c'est une liste avec info de 11 films (le premier est le film qui étais choisi au debut), dans cette liste il y a 11 listes
    #chaque de cette liste a dans l'order suivent: titre, année de production, rating, popularity, genres et chemin URL (attention ce n'est pas un chemin coplet il faut ajouter le debut de site tmdf dans le code html)
    liste_ml = []
    for id in film_id:
        if int(id) != int(movie_id):
            list_temp = []
            list_temp.append(df_films_info[df_films_info['id']==int(id)]['primaryTitle'].values[0])
            list_temp.append(df_films_info[df_films_info['id']==int(id)]['averageRating'].values[0])
            list_temp.append(df_films_info[df_films_info['id']==int(id)]['poster_path'].values[0])
            list_temp.append(df_films_info[df_films_info['id']==int(id)]['id'].values[0])
            liste_ml.append(list_temp)

    return render_template('movie.html', title='Movie', movies=movie_info, director=crew_list, actors=actor_list, value_ml=liste_ml)


# Searchbar Page

from flask import redirect, url_for, render_template

@bp.route('/search', methods=['GET'])
def show_search_page():
    return render_template('searchbar.html')

@bp.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query')

    #movie_data = df_films_info[df_films_info['primaryTitle'].str.contains(search_query, case=False)].sort_values(by=["popularity"], ascending=False).iloc[0]['id']
    #if not movie_data.empty:
        # Si un film correspondant est trouvé dans la base de données
       # movie_id = movie_data.iloc[0]['id']  # Supposons que 'id' soit la colonne contenant les IDs des films
    #if movie_data:
        
        # Redirection vers la page 'movie.html' avec l'ID du film trouvé
    #    return redirect(url_for('main.movie', movie_id=movie_data))
    #else:
        # Gérer le cas où aucun film correspondant n'est trouvé
    #    return render_template('error.html', error_message='Movie not found'), 404

    movie_data = df_films_info[df_films_info['primaryTitle'].str.contains(search_query, case=False)].sort_values(by=["popularity"], ascending=False)

    if not movie_data.empty:        
        movie_id = movie_data.iloc[0]['id']  # Supposons que 'id' soit la colonne contenant les IDs des films

        # Redirection vers la page 'movie.html' avec l'ID du film trouvé
        return redirect(url_for('main.movie', movie_id=movie_id))
    else:
        # Aucun film correspondant n'est trouvé, afficher la page 'searchbar.html'
        return render_template('error.html')
    
@bp.route('/credits')
def credits():
     return render_template('credit.html')

    
@bp.route('/signUp')
def signUp():
     return render_template('sign-up.html')