import os

from matplotlib.pylab import acorr

ETL_DIRECTORY = "etl_files"
ACTORS_CSV = "actors.csv"

if ETL_DIRECTORY not in  os.listdir():
    os.mkdir(ETL_DIRECTORY)
    print("ETL Directory Created")

if os.listdir(ETL_DIRECTORY) == []:
    for i in range(5):
        file = open(f"{ETL_DIRECTORY}/etapa-{i + 1}.txt", "x")
        file.close()
    print("Files Created")

# ETAPA 1

with open(ACTORS_CSV, "r") as file:
    actors = {}

    for line in file.readlines():
        if '"' in line:
            csv = []
            csv.append(line.split('"')[1])
            csv += line.split('"')[2].split(",")[1:]
        else:
            csv = line.split(',')
        if csv[0] == "Actor":
            continue

        if csv[0] not in actors.keys():
            actors[csv[0]] = float((csv[2]).strip())
    the_actor = ""
    movie_quantity = 0
    for actor in actors.keys():
        if actors[actor] > movie_quantity:
            movie_quantity = actors[actor]
            the_actor = actor

    print(f"O Ator/Atriz com maior Numero de filmes é {the_actor} com {movie_quantity} Filmes")

with open(ACTORS_CSV, "r") as file:
    movies = {}

    for line in file.readlines():
        if '"' in line:
            csv = []
            csv.append(line.split('"')[1])
            csv += line.split('"')[2].split(",")[1:]
        else:
            csv = line.split(',')
        if csv[0] == "Actor":
            continue
        
        if csv[4] not in movies.keys():
            movies[csv[4]] = [float(csv[5].strip())]
        else:
            movies[csv[4]].append(float(csv[5].strip()))
    for movie in movies.keys():
        mean = sum(movies[movie])/len(movies[movie])
        
        print(f"Filme: {movie}, Media de Receita: ${mean: .2f}")
    

