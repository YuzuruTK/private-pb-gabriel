import boto3 as b3
import datetime
import json
import requests
import time
import os

# Constants of the project
BUCKET_NAME = "data-lake-do-gabriel-buron"
LOTR_IDS = ["tt0120737", "tt0167260","tt0167261", "tt0903624", "tt1170358", "tt2310332"]

API_TOKEN = os.environ["API_TOKEN"]
API_KEY = os.environ["API_KEY"]

date = datetime.datetime.now()

# Boto3 objects
s3 = b3.client('s3', region_name='us-west-2')

JSON_PATH = f"Raw/TMDB/JSON/{date.year}/{date.month}/{date.day}"
# Get TMDB Ids of the movies that i have the IMDB id

lotr_tmdb_ids = []
movies_ids = []


headers = {"accept" : "application/json",
           "Authorization" : f"Bearer {API_TOKEN}",
           }

def request_tmdb_id():
    index = 0
    print("Requesting TMDB IDs")
    for id in LOTR_IDS:
        url = f"https://api.themoviedb.org/3/find/{id}"
        params = {
            "external_source" : "imdb_id"
            }
        
        response = requests.get(url, headers=headers, params=params)
        movie_id = response.json()['movie_results'][0]['id']

        index += 1
        print(f"Requests made: {index}/{len(LOTR_IDS)}", end="\r")
        
        lotr_tmdb_ids.append(movie_id)
    print("\nIDs Request Done")

def request_movie_details():
    index = 0
    movies = []
    print("Requesting LOTR movie Details")
    for id in lotr_tmdb_ids:
        url = f"https://api.themoviedb.org/3/movie/{id}"
        url2 = f"https://api.themoviedb.org/3/movie/{id}/keywords"

        response = requests.get(url, headers=headers)
        keywords_response = requests.get(url2, headers=headers)
        
        movie = response.json()
        movie["keywords"] =  [word["name"] for word in keywords_response.json()["keywords"]]
        movies.append(movie)
        index += 1
        print(f"Requests made: {index}/{len(lotr_tmdb_ids)}", end="\r")
    data = json.dumps({"movies" : movies},indent=4)
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/details/movie_details.json", Body=data)
    except Exception as e:
        print(e)
    print("\nAll Movie Details get")
    

def request_movies_before_lotr():
    index = 0
    registers = 0
    files_id = 0
    movies = []
    start_time = time.time()
    print("Requesting Movies before LOTR\n")
    while True:
        url = "https://api.themoviedb.org/3/discover/movie"
        index+= 1

        if index > 500:
            print("\nTheres no More Pages")
            break  

        params = {
            "with_genres": 14,
            "release_date.lte": "2001-12-17",
            "release_date.gte": "1981-12-17",
            "page": index,
            "sort" : "primary_release_date.desc"
            }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Server Error: {response.status_code}")
            print(response.json()["status_message"])
            break

        if response.json()["total_pages"] == index:
            print("\nThere is no more Movies")
            break
        for movie in response.json()["results"]:
            if registers >= 100:
                data = json.dumps({"results" : movies},indent=4)
                s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/movies/movies_before_{files_id}.json", Body=data)
                files_id += 1
                movies.clear()
                registers = 0
            registers += 1
            # Get Only the info that i want
            movie_info = {}
            movie_info["id"] = movie["id"]
            movie_info["overview"] = movie["overview"]
            movie_info["popularity"] = movie["popularity"]
            movie_info["title"] = movie["title"]
            movie_info["vote_average"] = movie["vote_average"]
            movie_info["vote_count"] = movie["vote_count"]
            movie_info["release_date"] = movie["release_date"]
            # Get ONLY the movies with rating over 7 and count over 1000, popular and good movies i guess
            if movie_info["vote_average"] > 7 and movie_info["vote_count"] > 1000:
                movies_ids.append(movie["id"])
            movies.append(movie_info)
        # Put the rest of movies of the last page on a Json file
        data = json.dumps({"results" : movies},indent=4)
        s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/movies/movies_before_{files_id}.json", Body=data)
        print(f"Requests made: {index} --- {time.time() - start_time:.2f} seconds passed", end="\r")
    print(f"\nRequest to get All Fantasy Movies before LOTR Done in {time.time() - start_time:.2f} seconds")

def request_movies_after_lotr():    
    index = 0
    registers = 0
    files_id = 0
    movies = []
    start_time = time.time()
    while True:
        url = "https://api.themoviedb.org/3/discover/movie"
        index+= 1
        if index > 500:
            print("\nTheres no More Pages")
            break

        params = {
            "with_genres": 14,
            "release_date.gte": "2001-12-17",
            "release_date.lte": "2021-12-17",
            "page": index,
            "sort" : "primary_release_date.desc"
            }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"\nServer Error: {response.status_code}")
            print(response.json()["status_message"])
            print(f"index {index}")
            break
        if response.json()["total_pages"] == index:
            print("\nThere is no more Movies")
            break

        for movie in response.json()["results"]:
            if registers >= 100:
                data = json.dumps({"results" : movies},indent=4)
                s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/movies/movies_after_{files_id}.json", Body=data)
                files_id += 1
                movies.clear()
                registers = 0
            registers += 1

            # Get Only the info that i want
            movie_info = {}
            movie_info["id"] = movie["id"]
            movie_info["overview"] = movie["overview"]
            movie_info["popularity"] = movie["popularity"]
            movie_info["title"] = movie["title"]
            movie_info["vote_average"] = movie["vote_average"]
            movie_info["vote_count"] = movie["vote_count"]
            movie_info["release_date"] = movie["release_date"]
            # Get ONLY the movies with rating over 7 and count over 1000, popular and good movies i guess
            if movie_info["vote_average"] > 7 and movie_info["vote_count"] > 1000:
                movies_ids.append(movie["id"])
            movies.append(movie_info)
        # Put the rest of movies of the last page on a Json file
        data = json.dumps({"results" : movies},indent=4)
        s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/movies/movies_after_{files_id}.json", Body=data)
        print(f"Requests made: {index} --- {time.time() - start_time:.2f} seconds passed", end="\r")
    print(f"\nRequest to get All Fantasy Movies after LOTR Done in {time.time() - start_time:.2f} seconds")

def get_all_keywords():
    index = 0
    registers = 0
    keywords = []
    start_time = time.time()
    print("Getting all KeyWords")
    for id in movies_ids:
        registers += 1

        url2 = f"https://api.themoviedb.org/3/movie/{id}/keywords"
        keywords_response = requests.get(url2, headers=headers)
        
        if registers >= 100:
            data = json.dumps({"keywords" : keywords},indent=4)
            s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/keywords/keywords_{index}.json", Body=data)
            index += 1
            keywords.clear()
            registers = 0
        lista = [word["name"] for word in keywords_response.json()["keywords"]]
        if len(lista) != 0:
            keywords.append(lista)
        print(f"Requests made: {registers + (100*index)} --- {time.time() - start_time:.2f}", end="\r")
    # Put the rest of keywords of the last page on a Json file
    data = json.dumps({"keywords" : keywords},indent=4)
    s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/keywords/keywords_{index}.json", Body=data)
    print(f"\nKeywords Requests Done in {time.time() - start_time:.2f} seconds")


def lambda_handler(event, context):
    try:
        request_tmdb_id()
        request_movie_details()
        request_movies_after_lotr()
        request_movies_before_lotr()
        get_all_keywords()
        return {
            'statusCode' : 200,
            'body' : json.dumps("All Data Saved on Bucket")
        }
    except Exception as ex:
        return {
            'statusCode' : 500,
            'body' : json.dumps(f"Error Saving the Files on Bucket: \n{ex}")
        }