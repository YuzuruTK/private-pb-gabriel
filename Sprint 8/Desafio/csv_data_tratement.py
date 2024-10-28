import sys
from datetime import date
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, when
from pyspark.sql.types import IntegerType, FloatType
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

# Constants
date = date.today()
INPUT_PATH = "s3://data-lake-do-gabriel-buron/Raw/Local/CSV/Movies/2024/9/8/movies.csv"
OUTPUT_PATH = f"s3://data-lake-do-gabriel-buron/TRUSTED/CSV/{date.year}/{date.month}/{date.day}/"

# Glue Settings

glueContext = GlueContext(SparkContext())
spark = glueContext.spark_session
job = Job(glueContext)
job.init('data_treatment_csv', {})

print("Job Started")

# Getting CSV data
input_dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3", 
    connection_options={"paths": [INPUT_PATH]}, 
    format="csv", 
    format_options={"withHeader": True, "separator": "|"}
)
df = input_dynamic_frame.toDF()
print("Dataframe Imported")

# Data Tratement
df = df.toDF(*(c.replace("|", "").replace(" ", "_") for c in df.columns))

df = df.filter((col("anoLancamento") > 1980) & (col("anoLancamento") <= 2020))
df = df.filter((col("genero").contains("Fantasy")))

df = df.drop("generoArtista")
df = df.drop("personagem")
df = df.drop("nomeArtista")
df = df.drop("anoNascimento")
df = df.drop("anoFalecimento")
df = df.drop("profissao")
df = df.drop("titulosMaisConhecidos")

df = df.withColumn("anoLancamento", col("anoLancamento").cast(IntegerType()))
df = df.withColumn("tempoMinutos", col("tempoMinutos").cast(IntegerType()))
df = df.withColumn("notaMedia", col("notaMedia").cast(FloatType()))
df = df.withColumn("numeroVotos", col("numeroVotos").cast(IntegerType()))

df = df.withColumn("tempoMinutos", when(col("tempoMinutos").isNull(), 0).otherwise(col("tempoMinutos")))

print("Dataframe cleaned")

# Putting trated data into bucket
df_output = DynamicFrame.fromDF(df, glueContext, "output_dynamic_frame")

glueContext.write_dynamic_frame.from_options(
    frame = df_output,
    connection_type = "s3",
    connection_options = {"path": OUTPUT_PATH},
    format = "parquet"
)

print("Parquet created")
job.commit()