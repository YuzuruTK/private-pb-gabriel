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
DATE = datetime.datetime.now()
JSON_PATH = f"Raw/TMDB/JSON/{DATE.year}/{DATE.month}/{DATE.day}"

# Boto3 objects
s3 = b3.client('s3', region_name='us-west-2')

# Header of Requisition
headers = {"accept" : "application/json",
           "Authorization" : f"Bearer {API_TOKEN}",
           }

# List used to save the IDS of TMDB from lotr movies
lotr_tmdb_ids = []
# List used to save the Movies that have High Aprove to get Keywords Later
movies_ids = []

# Get TMDB Ids of the movies that i have the IMDB id
def request_tmdb_id():
    index = 0
    print("Requesting TMDB IDs")

    for id in LOTR_IDS:
        url = f"https://api.themoviedb.org/3/find/{id}"
        # Defining the source of the id sent
        params = {
            "external_source" : "imdb_id"
            }
        
        response = requests.get(url, headers=headers, params=params)
        # extracting the ID of the movie
        movie_id = response.json()['movie_results'][0]['id']

        index += 1
        print(f"Requests made: {index}/{len(LOTR_IDS)}", end="\r")
        # Adding the id to the list
        lotr_tmdb_ids.append(movie_id)
    print("\nIDs Request Done")

# Getting the Details from the LOTR movies
def request_movie_details():
    index = 0
    movies = []
    print("Requesting LOTR movie Details")
    for id in lotr_tmdb_ids:
        # URL to get the Details from a Movie
        url = f"https://api.themoviedb.org/3/movie/{id}"
        # URL to get the Keywords from the Movie
        url2 = f"https://api.themoviedb.org/3/movie/{id}/keywords"

        response = requests.get(url, headers=headers)
        keywords_response = requests.get(url2, headers=headers)
        
        # Passing all the info to a variable
        movie = response.json()
        # Adding the Keywords to this variable to append information
        movie["keywords"] =  [word["name"] for word in keywords_response.json()["keywords"]]
        # Apeending to the movies 
        movies.append(movie)
        index += 1
        print(f"Requests made: {index}/{len(lotr_tmdb_ids)}", end="\r")
    # Trowing the list to a JSON
    data = json.dumps({"movies" : movies},indent=4)
    # Putting the JSON on the bucket
    s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/movie_details.json", Body=data)
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
        
        # Theres a Max Limit of pages in TMDB, and it is 500
        if index > 500:
            print("\nTheres no More Pages")
            break  

        # Setting the parameters to a refined search
        params = {
            "with_genres": 14,
            "release_date.lte": "2001-12-17",
            "release_date.gte": "1981-12-17",
            "page": index,
            "sort" : "primary_release_date.desc"
            }
        
        response = requests.get(url, headers=headers, params=params)
        
        # If there is an Error it will print and then Break the While loop
        if response.status_code != 200:
            print(f"Server Error: {response.status_code}")
            print(response.json()["status_message"])
            break
        
        # If it reachs the same pages as total, then it has no movies to search and will break the loop
        if response.json()["total_pages"] == index:
            print("\nThere is no more Movies")
            break

        for movie in response.json()["results"]:
            # Case there is already 100 registers on the memory it will create a JSON file on bucket and clear the list
            if registers >= 100:
                data = json.dumps({"results" : movies},indent=4)
                s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/movies_before_{files_id}.json", Body=data)
                files_id += 1
                movies.clear()
                registers = 0
            
            # Getting Only the info that i want
            registers += 1
            movie_info = {}
            movie_info["id"] = movie["id"]
            movie_info["overview"] = movie["overview"]
            movie_info["popularity"] = movie["popularity"]
            movie_info["title"] = movie["title"]
            movie_info["vote_average"] = movie["vote_average"]
            movie_info["vote_count"] = movie["vote_count"]
            # Get ONLY the movies with rating over 7 and count over 1000, popular and good movies i guess
            if movie_info["vote_average"] > 7 and movie_info["vote_count"] > 1000:
                movies_ids.append(movie["id"])
            movies.append(movie_info)
        # Put the rest of movies of the last page on a Json file
        data = json.dumps({"results" : movies},indent=4)
        s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/movies_before_{files_id}.json", Body=data)
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
        # Theres a Max Limit of pages in TMDB, and it is 500
        if index > 500:
            print("\nTheres no More Pages")
            break

        # Setting the parameters to a refined search
        params = {
            "with_genres": 14,
            "release_date.gte": "2001-12-17",
            "release_date.lte": "2021-12-17",
            "page": index,
            "sort" : "primary_release_date.desc"
            }
        
        response = requests.get(url, headers=headers, params=params)
        
        # If there is an Error it will print and then Break the While loop
        if response.status_code != 200:
            print(f"\nServer Error: {response.status_code}")
            print(response.json()["status_message"])
            print(f"index {index}")
            break

        # If it reachs the same pages as total, then it has no movies to search and will break the loop
        if response.json()["total_pages"] == index:
            print("\nThere is no more Movies")
            break

        for movie in response.json()["results"]:
            # Case there is already 100 registers on the memory it will create a JSON file on bucket and clear the list
            if registers >= 100:
                data = json.dumps({"results" : movies},indent=4)
                s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/movies_after_{files_id}.json", Body=data)
                files_id += 1
                movies.clear()
                registers = 0

            # Get Only the info that i want
            registers += 1
            movie_info = {}
            movie_info["id"] = movie["id"]
            movie_info["overview"] = movie["overview"]
            movie_info["popularity"] = movie["popularity"]
            movie_info["title"] = movie["title"]
            movie_info["vote_average"] = movie["vote_average"]
            movie_info["vote_count"] = movie["vote_count"]
            # Get ONLY the movies with rating over 7 and count over 1000, popular and good movies i guess
            if movie_info["vote_average"] > 7 and movie_info["vote_count"] > 1000:
                movies_ids.append(movie["id"])
            movies.append(movie_info)
        # Put the rest of movies of the last page on a Json file
        data = json.dumps({"results" : movies},indent=4)
        s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/movies_after_{files_id}.json", Body=data)
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
        # Case there is already 100 registers on the memory it will create a JSON file on bucket and clear the list
        if registers >= 100:
            data = json.dumps({"keywords" : keywords},indent=4)
            s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/keywords_{index}.json", Body=data)
            index += 1
            keywords.clear()
            registers = 0
        # Extract only the names of the Keywords to group them in a JSON
        lista = [word["name"] for word in keywords_response.json()["keywords"]]
        # if there is no words on the list then it will not be appended
        if len(lista) != 0:
            keywords.append(lista)
        print(f"Requests made: {registers + (100*index)} --- {time.time() - start_time:.2f}", end="\r")
    # Put the rest of keywords of the last page on a Json file
    data = json.dumps({"keywords" : keywords},indent=4)
    s3.put_object(Bucket=BUCKET_NAME, Key=f"{JSON_PATH}/keywords_{index}.json", Body=data)
    print(f"\nKeywords Requests Done in {time.time() - start_time:.2f} seconds")


def lambda_handler(event, context):
    try:
        # Requests the IDs of Lotr movies
        request_tmdb_id()
        # Get the Details fo this movies
        request_movie_details()
        # Get all the movies and some info about them after the 1th movie of LOTR has launched
        request_movies_after_lotr()
        # Get all the movies and some info about them before the 1th movie of LOTR has launched
        request_movies_before_lotr()
        # Get all the keywords of the movies that has good review of the lists above
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