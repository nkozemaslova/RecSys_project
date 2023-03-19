import pandas as pd
from sklearn.cluster import KMeans

#отбираем столбцы с звуковыми характеристиками песен
audio_features_data = data[['acousticness', 'valence','danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo']]

# выделяем 10 кластеров
kmeans = KMeans(n_clusters=10, random_state=42)
kmeans.fit(audio_features_data)

# добавляем колонку с кластером к оригинальному датасету
audio_features_data['cluster'] = kmeans.labels_
data['cluster'] = kmeans.labels_

def recommend_track(track_name, number_of_tracks=10):
    # выделяем характеристики трека, заданного пользователем
    input_track_features = data.loc[
        data['track_name'] == track_name, ['acousticness', 'valence', 'danceability', 'energy', 'instrumentalness',
                                           'liveness', 'loudness', 'speechiness', 'tempo']].values
    # предсказываем кластер
    input_track_cluster = kmeans.predict(input_track_features)[0]

    # рекомендуем треки из кластера
    recommendations = data[data['cluster'] == input_track_cluster].sample(number_of_tracks)[
        ['track_name', 'artist_name']].values
    recommendations = pd.DataFrame(recommendations, columns=['Track name', 'Artist name'])
    recommendations = recommendations.drop_duplicates()

    return recommendations.head(number_of_tracks)

recommend_track('Quand je monte chez toi')