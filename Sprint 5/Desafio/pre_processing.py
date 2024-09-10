import pandas as pd
import boto3 as b3

# Constants of the project
CSV_PATH = "sustentabilidade_-_agua_2022.csv"
BUCKET_NAME = "desafio-sprint-5-compasso"
PROFILE = "009160031919_AdministratorAccess"
CSV_BUCKET_NAME = "data.csv"
OUTPUT_PATH = "./output_csv/"

# Boto3 objects
session = b3.Session(profile_name=PROFILE)
s3 = session.resource("s3")
bucket = s3.Bucket(BUCKET_NAME)

# Adjusting CSV file
months = {"Janeiro": 1,"Fevereiro": 2,"Março": 3,"Abril": 4,"Maio": 5,"Junho": 6,"Julho": 7,"Agosto": 8,"Setembro": 9,"Outubro": 10,"Novembro": 11,"Dezembro": 12}

print("Lendo o arquivo...")
df = pd.read_csv(CSV_PATH, low_memory=False, encoding="latin-1", delimiter=";")
df = df.dropna()
df["Mes"] = df["Mes"].apply(lambda x: months[x.strip()])
print("Ajustes feitos com sucesso!")
print(f"Tamanho do DataFrame: {len(df)}\n")
print(df.head(5).to_markdown())

print("Salvando o arquivo...")
df.to_csv(OUTPUT_PATH+CSV_BUCKET_NAME, index=False, encoding="utf-8")
print("Arquivo salvo com sucesso!")
print("Enviando arquivo para o bucket...")
bucket.upload_file(OUTPUT_PATH+CSV_BUCKET_NAME,CSV_BUCKET_NAME)
print("Arquivo enviado com sucesso!")