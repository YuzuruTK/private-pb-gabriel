import boto3 as b3
import datetime
import json
import requests
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

lotr_tmdb_ids = [] #[120, 122, 121, 49051, 57158, 122917]

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

headers = {"accept" : "application/json",
           "Authorization" : f"Bearer {API_TOKEN}",
           }


def lambda_handler(event, context):
    try:
        request_tmdb_id()
        request_movie_details()

        return {
            'statusCode' : 200,
            'body' : json.dumps("All Data Saved on Bucket")
        }
    except Exception as ex:
        return {
            'statusCode' : 500,
            'body' : json.dumps(f"Error Saving the Files on Bucket: \n{ex}")
        }