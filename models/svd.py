import numpy as np
import pandas as pd
import math

from sklearn.model_selection import train_test_split
from tqdm import tqdm_notebook
from scipy.linalg import svd

#подготовка данных

#срез из небольшого количества данных для тестирования алгоритма
df = data[:200000]

df.drop(labels = ['genre', 'artist_name', 'track_id', 'popularity',
       'acousticness', 'danceability', 'duration_ms', 'energy',
       'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
       'speechiness', 'tempo', 'time_signature', 'valence'], axis = 1, inplace = True)

df.playlistname = 1

#решение проблемы холодного старта, пользователи с 5 и более треками в плейлисте
users_interactions_count_df = (
    df
    .groupby(['user_id', 'track_name'])
    .first()
    .reset_index()
    .groupby('user_id').size())
print('# users:', len(users_interactions_count_df))

users_with_enough_interactions_df = \
    users_interactions_count_df[users_interactions_count_df >= 5].reset_index()[['user_id']]
print('# users with at least 5 interactions:',len(users_with_enough_interactions_df))

interactions_from_selected_users_df = df.loc[np.in1d(df.user_id,
            users_with_enough_interactions_df)]

#применение взвешенного рейтинга
def smooth_user_preference(x):
    return math.log(1 + x, 2)

interactions_full_df = (
    interactions_from_selected_users_df
    .groupby(['user_id', 'track_name']).playlistname.sum()
    .apply(smooth_user_preference)
    .reset_index().set_index(['user_id', 'track_name'])
)

interactions_full_df = interactions_full_df.reset_index()
interactions_full_df.head(20)

#train/test split
interactions_train_df, interactions_test_df = train_test_split(interactions_full_df,
                                   stratify=interactions_full_df['user_id'],
                                   test_size=0.25,
                                   random_state=42)

print('# interactions on Train set: %d' % len(interactions_train_df))
print('# interactions on Test set: %d' % len(interactions_test_df))

interactions = (
    interactions_train_df
    .groupby('user_id')['track_name'].agg(lambda x: list(x))
    .reset_index()
    .rename(columns={'track_name': 'true_train'})
    .set_index('user_id')
)

interactions['true_test'] = (
    interactions_test_df
    .groupby('user_id')['track_name'].agg(lambda x: list(x))
)

# заполнение пропусков пустыми списками
interactions.loc[pd.isnull(interactions.true_test), 'true_test'] = [
    [''] for x in range(len(interactions.loc[pd.isnull(interactions.true_test), 'true_test']))]

interactions.head(5)

#Матрица "оценок" пользователей. Нули будут обозначать отсутствие взаимодействия.

ratings = pd.pivot_table(
    interactions_train_df,
    values='playlistname',
    index='user_id',
    columns='track_name').fillna(0)

ratings = ratings[:3000]
interactions = interactions[:3000]
top_k = 10

U, sigma, V = svd(ratings)
print(ratings.shape, U.shape, sigma.shape, V.shape)

Sigma = np.zeros((3000, 6121))
Sigma[:3000, :3000] = np.diag(sigma)

new_ratings = U.dot(Sigma).dot(V)

print(sum(sum((new_ratings - ratings.values) ** 2)))

K = 100

sigma[K:] = 0
Sigma = np.zeros((3000, 6121))
Sigma[:3000, :3000] = np.diag(sigma)

new_ratings = U.dot(Sigma).dot(V)

print(sum(sum((new_ratings - ratings.values) ** 2)))
print(sum(sum((ratings.values.mean() - ratings.values) ** 2)))

new_ratings = pd.DataFrame(new_ratings, index=ratings.index, columns=ratings.columns)

predictions = []

for personId in tqdm_notebook(interactions.index):
    prediction = (
        new_ratings
        .loc[personId]
        .sort_values(ascending=False)
        .index.values
    )

    predictions.append(
        list(prediction[~np.in1d(
            prediction,
            interactions.loc[personId, 'true_train'])])[:top_k])

interactions['prediction_svd'] = predictions

#реализация метрики
def calc_precision(column):
    return (
        interactions
        .apply(
            lambda row:
            len(set(row['true_test']).intersection(
                set(row[column]))) /
            min(len(row['true_test']) + 0.001, 10.0),
            axis=1)).mean()

#результаты по метрике
calc_precision('prediction_svd')


