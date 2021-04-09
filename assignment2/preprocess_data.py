import pandas as pd 
import time

data_filename = 'anime.csv'

df = pd.read_csv(data_filename)

print(df.head())

def format_duration(x):
    numbers = [int(s) for s in x.split() if s.isdigit()]
    minutes = 0
    if len(numbers) == 2:
        return numbers[0] * 60 + numbers[1]
    elif len(numbers) == 1:
        return numbers[0]
    else:
        return "null"


def format_list(x):
    if x.strip() == "-":
        return "null"
    else:
        x.replace('\xa0Adventure', "Adventure")
        list_x = x.lower().split(",")
        # list_x = ["'" + i + "'" for i in list_x]
        string_builder = ",".join(list_x)
        string_builder = "{" + string_builder + "}"
        return string_builder

def format_broadcast(x):
    if "Sunday" in x:
        return 0
    elif "Monday" in x:
        return 1
    elif "Tuesday" in x:
        return 2
    elif "Wednesday" in x:
        return 3
    elif "Thursday" in x:
        return 4
    elif "Friday" in x:
        return 5
    elif "Saturday" in x:
        return 6
    else:
        return "null"

def clean_null(x):
    if x == "-":
        return "null"
    else:
        return x

set_genres = set()
for i in df['Genres']:
    genres = i.split(',')
    for g in genres:
        set_genres.add(g.lower())
        
set_genres = sorted(set_genres)
print(set_genres)

df['Duration'] = df['Duration'].apply(format_duration)
df['Producers'] = df['Producers'].apply(format_list)
df['Genres'] = df['Genres'].apply(format_list)
df['Licensors'] = df['Licensors'].apply(format_list)
df['Broadcast time'] = df['Broadcast time'].apply(format_broadcast)
df['Start airing'] = df['Start airing'].apply(clean_null)
df['End airing'] = df['End airing'].apply(clean_null)
df['Starting season'] = df['Starting season'].apply(clean_null)
df['Episodes'] = df['Episodes'].apply(clean_null)
df = df.drop(columns=['Description'])

df.to_csv(r'anime_processed.csv', index = False, header=True)
