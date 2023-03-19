import pandas as pd

def dict_from_data(data):

    data = data.drop(labels = ['genre', 'artist_name', 'track_id', 'popularity',
                               'acousticness', 'danceability', 'duration_ms', 'energy',
                               'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
                               'speechiness', 'tempo', 'time_signature', 'valence',
                               'playlistname'], axis = 1)
    d = {}
    for i in data['user_id'].unique():
        d[i] = {data['track_name'][j]: 1 for j in data[data['user_id' ]= =i].index}

    return d

def get_pop_songs(d):
    songs_rating = {}
    for user, songs in d.items():
        for song, _ in songs.items():
            songs_rating.setdefault(song, 0)  # поставили каждой песне частоту встречаемости 0
            songs_rating[song] += 1  # если песня встречается больше одного раза увеличиваем счетчик
    songs_rating = dict(sorted(songs_rating.items(), key=lambda x: x[1], reverse=True))  # отсортированный словарь по убыванию рейтинга (частоты встречаемости) песен
    return songs_rating


def top_pop_recommender(d, user):
    recoms = get_pop_songs(d)
    recoms = {k: v for k, v in recoms.items() if k not in d[user]}
    return recoms

#данные в формате словаря
d = dict_from_data(data)

#самые популярные песни и кол-во их добавлений в плейлисты
get_pop_songs(d)

#рекомендация для конкретного user_id
top_pop_recommender(d, 'e897138cc060faf75a4a3d56c6ce2af1')