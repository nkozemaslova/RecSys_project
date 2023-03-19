import numpy as np
import pandas as pd
import math

from sklearn.model_selection import train_test_split
from tqdm import tqdm_notebook
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

ratings_m = ratings.values

similarity_users = np.zeros((len(ratings_m), len(ratings_m)))

for i in tqdm_notebook(range(len(ratings_m) - 1)):
    for j in range(i + 1, len(ratings_m)):

        # nonzero elements of two users
        mask_uv = (ratings_m[i] != 0) & (ratings_m[j] != 0)

        # continue if no intersection
        if np.sum(mask_uv) == 0:
            continue

        # get nonzero elements
        ratings_v = ratings_m[i, mask_uv]
        ratings_u = ratings_m[j, mask_uv]

        # for nonzero std
        if len(np.unique(ratings_v)) < 2 or len(np.unique(ratings_u)) < 2:
            continue

        similarity_users[i, j] = np.corrcoef(ratings_v, ratings_u)[0, 1]
        similarity_users[j, i] = similarity_users[i, j]

prediction_user_based = []

for i in tqdm_notebook(range(len(similarity_users))):

    users_sim = similarity_users[i] > 0

    if len(users_sim) == 0:
        prediction_user_based.append([])
    else:
        tmp_recommend = np.argsort(ratings_m[users_sim].sum(axis=0))[::-1]
        tmp_recommend = ratings.columns[tmp_recommend]
        recommend = np.array(tmp_recommend)[~np.in1d(tmp_recommend, interactions.iloc[i])][:10]
        prediction_user_based.append(list(recommend))

interactions['prediction_user_based'] = prediction_user_based

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
calc_precision('prediction_user_based')