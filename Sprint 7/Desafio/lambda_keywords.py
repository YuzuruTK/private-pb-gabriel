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

lotr_tmdb_ids = [] #[120, 122, 121, 49051, 57158, 122917]

# Get the list from bucket
response = s3.get_object(Bucket=BUCKET_NAME, Key=(JSON_PATH + "/movies_id.json"))
file_content = response['Body'].read().decode('utf-8')
movies_ids = json.loads(file_content)    

headers = {"accept" : "application/json",
           "Authorization" : f"Bearer {API_TOKEN}",
           }


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
            keywords.append({id : lista})
        print(f"Requests made: {registers + (100*index)} --- {time.time() - start_time:.2f}", end="\r")
    # Put the rest of keywords of the last page on a Json file
    data = json.dumps({"keywords" : keywords},indent=4)
    s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/keywords/keywords_{index}.json", Body=data)
    print(f"\nKeywords Requests Done in {time.time() - start_time:.2f} seconds")


def lambda_handler(event, context):
    try:
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