import boto3 as b3
import datetime
import json
import requests
import time
import os

# Constants of the project
BUCKET_NAME = "data-lake-do-gabriel-buron"

API_TOKEN = os.environ["API_TOKEN"]
API_KEY = os.environ["API_KEY"]

date = datetime.datetime.now()

# Boto3 objects
s3 = b3.client('s3', region_name='us-west-2')

JSON_PATH = f"Raw/TMDB/JSON/{date.year}/{date.month}/{date.day}"
# Get TMDB Ids of the movies that i have the IMDB id

lotr_tmdb_ids = [] #[120, 122, 121, 49051, 57158, 122917]
movies_ids = []


headers = {"accept" : "application/json",
           "Authorization" : f"Bearer {API_TOKEN}",
           }

def request_fantasy_movies():
    index = 0
    registers = 0
    files_id = 0
    movies = []
    start_time = time.time()
    print("Requesting Fantasy Movies 10 years range on LOTR\n")
    while True:
        url = "https://api.themoviedb.org/3/discover/movie"
        index+= 1

        if index > 500:
            print("\nTheres no More Pages")
            break  

        params = {
            "with_genres": 14,
            "release_date.lte": "2021-12-17",
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
            print(response.json)
            print("\nThere is no more Movies")
            break
        
        for movie in response.json()["results"]:
            if registers >= 100:
                data = json.dumps({"results" : movies},indent=4)
                s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/movies/movies_{files_id}.json", Body=data)
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
        print(f"Requests made: {index} --- {time.time() - start_time:.2f} seconds passed", end="\r")
    # Put the rest of movies of the last page on a Json file
    data = json.dumps({"results" : movies},indent=4)
    s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/movies/movies_{files_id}.json", Body=data)
    # Getting id and throwing in the folder to get keywords later
    # s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/movies_id.json", Body=(json.dumps(movies_ids)))
    print(f"\nRequest to get All Fantasy Movies 10 years range LOTR Done in {time.time() - start_time:.2f} seconds")

def lambda_handler(event, context):
    try:
        request_fantasy_movies()
        return {
            'statusCode' : 200,
            'body' : json.dumps("All Data Saved on Bucket")
        }
    except Exception as ex:
        return {
            'statusCode' : 500,
            'body' : json.dumps(f"Error Saving the Files on Bucket: \n{ex}")
        }