import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

#кодируем категориальные столбцы key, mode, time_signature
list_of_keys = df['key'].unique()
for i in range(len(list_of_keys)):
  df.loc[df.key == list_of_keys[i], 'key'] = i

df.loc[df['mode']== 'Major', 'mode'] = 1
df.loc[df['mode']== 'Minor', 'mode'] = 0

list_of_time_signatures = df['time_signature'].unique()
for i in range(len(list_of_time_signatures)):
  df.loc[df['time_signature'] == list_of_time_signatures[i], 'time_signature'] = i

feature_cols=['acousticness', 'danceability', 'duration_ms', 'energy',
              'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
              'speechiness', 'tempo', 'time_signature', 'valence',]

scaler = MinMaxScaler()
normalized_df =scaler.fit_transform(df[feature_cols])

indices = pd.Series(df.index, index=df['track_name']).drop_duplicates()

cosine = cosine_similarity(normalized_df)


def generate_recommendation(track_name, model_type=cosine):
    """
    Purpose: Function for song recommendations
    Inputs: song title and type of similarity model
    Output: Pandas series of recommended songs
    """

    idx = indices[track_name]

    sim_scores = list(enumerate(model_type[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    songs_indices = [i[0] for i in sim_scores]

    return df['track_name'].iloc[songs_indices]

generate_recommendation('Tell Them Told You So', cosine)