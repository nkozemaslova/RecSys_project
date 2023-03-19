import pandas as pd
import math


#пользователь одну и ту же песню добавляет в разные плейлисты, можно учитывать это как взвешенный рейтинг
def smooth_user_preference(x):
    return math.log(1 + x, 2)

interactions_full_df = (
    df
    .groupby(['user_id', 'track_name']).playlistname.sum()
    .apply(smooth_user_preference)
    .reset_index().set_index(['user_id', 'track_name'])
)

df = interactions_full_df.reset_index()
df.sample(5)

d = {}
for i in df['user_id'].unique():
    d[i] = {df['track_name'][j]: df['playlistname'][j] for j in df[df['user_id']==i].index}

def sim_distance(d, person1, person2):
    sum_of_squares = sum([(d[person1][item] - d[person2][item])**2
                         for item in d[person1] if item in d[person2]])
    return 1/(1 + np.sqrt(sum_of_squares))

#схожесть двух пользователей
sim_distance(d,'3d0f759337e6aa576c75ecd3fbf14968','de05035bb2bba86bd702c3d54fc97e91')

#Сортировка пользователей на основе схожести
def sort_users(d, person, n=5, similarity=sim_distance):
    scores = [(other, round(similarity(d, person, other),2)) for other in d if other != person]
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores[:n]

sort_users(d,'3d0f759337e6aa576c75ecd3fbf14968', n=5)

#Рекомендации для схожих пользователей
def get_recoms_by_users(prefs, person, similarity=sim_distance):
    totals = {}
    sim_sums = {}
    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim

    rankings = [(item, round(total / sim_sums[item], 2)) for item, total in totals.items()]
    rankings = sorted(rankings, key=lambda x: x[1], reverse=True)

    return rankings

get_recoms_by_users(d, '3d0f759337e6aa576c75ecd3fbf14968', sim_distance)