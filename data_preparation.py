import pandas as pd

df = pd.read_csv('https://github.com/nkozemaslova/Data_2022/releases/download/data3/SpotifyFeatures.csv')
df.head()

df2 = pd.read_csv('https://github.com/nkozemaslova/Data_2022/releases/download/data4/spotify_dataset.csv',
                  skiprows=1,
                  names=['user_id', 'artistname', 'trackname', 'playlistname'],
                  on_bad_lines='skip')

# Переименовали колонку "artistname" во втором датасете на "artist_name"
df2 = df2.rename(columns={'artistname': 'artist_name'})

# Переименовали колнку "trackname" во втором датасете на "track_name"
df2 = df2.rename(columns={'trackname': 'track_name'})

#объединенный датасет
data = pd.merge(df, df2, on=['artist_name', 'track_name'], how='inner')