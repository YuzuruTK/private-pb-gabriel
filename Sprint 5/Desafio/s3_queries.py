import pandas as pd
import boto3 as b3
import time

# Constants of the project
BUCKET_NAME = "desafio-sprint-5-compasso"
PROFILE = "009160031919_AdministratorAccess"
CSV_BUCKET_NAME = "data.csv"
OUTPUT_PATH = "./output_csv/"
SQL_DIRECTORY = "./sql"

# Boto3 objects
session = b3.Session(profile_name=PROFILE)
s3 = session.resource("s3")
bucket = s3.Bucket(BUCKET_NAME)
select3 = session.client("s3")

# Function to convert s3 Responses to CSV
def response_to_csv(path, event_stream)-> str:
    actual_path = OUTPUT_PATH + path
    with open(actual_path, 'wb') as f:
        for event in event_stream:
            if 'Records' in event:
                data = event['Records']['Payload']
                f.write(data)
            elif 'Progress' in event:
                print(event['Progress']['Details'])
    return actual_path

init_time = time.time()
# First Query
sql = open(f"{SQL_DIRECTORY}/query_1.sql", "r").read()

response = select3.select_object_content(Bucket=BUCKET_NAME,
    Key=CSV_BUCKET_NAME,
    ExpressionType='SQL',
    Expression=sql,
    InputSerialization={'CSV': {"FileHeaderInfo": "USE"}},
    OutputSerialization={'CSV': {}},
)

csv_path = response_to_csv("output_1.csv", response["Payload"])
dataframe = pd.read_csv(csv_path, names=["Maximo", "Minimo"])

print(f"Query executada em:  {time.time() - init_time: .2f}s")
print("Quantidade Máxima e Minima de consumo de Agua em Janeiro de 2022: \n")
print(dataframe.head(10).to_markdown(index=False))

init_time = time.time()
# Second Query
sql = open(f"{SQL_DIRECTORY}/query_2.sql", "r").read()

response = select3.select_object_content(Bucket=BUCKET_NAME,
    Key=CSV_BUCKET_NAME,
    ExpressionType='SQL',
    Expression=sql,
    InputSerialization={'CSV': {"FileHeaderInfo": "USE"}},
    OutputSerialization={'CSV': {}},
)

csv_path = response_to_csv("output_2.csv", response["Payload"])
dataframe = pd.read_csv(csv_path, names=["Cidade - Campus","Quantidade M3", "Data"])

print(f"\n\nQuery executada em:  {time.time() - init_time: .2f}s")
print("Quantidade de M3 de agua por Campus e Data em Uberlândia: \n")
print(dataframe.head(100).to_markdown(index=False))
