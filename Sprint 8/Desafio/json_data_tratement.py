import sys
from datetime import date
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, explode, expr
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

# Constants
date = date.today()
INPUT_PATH = f"s3://data-lake-do-gabriel-buron/Raw/TMDB/JSON/{date.year}/{date.month}/{date.day}/"
OUTPUT_PATH = "s3://data-lake-do-gabriel-buron/TRUSTED/"

# Glue Settings
glueContext = GlueContext(SparkContext())
spark = glueContext.spark_session
job = Job(glueContext)
job.init('json_data_tratement', {})

# Reading Json
input_dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3", 
    connection_options={"paths": [INPUT_PATH+"details/movie_details.json"]}, 
    format="json", 
    format_options={"multiline": True}
)

df = input_dynamic_frame.toDF()
print("Dataframe Imported")

df = df.select(explode(col("movies")).alias("movie"))

df = df.select(
    col("movie.id").alias("id"),
    col("movie.title").alias("title"),
    col("movie.overview").alias("overview"),
    col("movie.release_date").alias("release_date"),
    col("movie.vote_average").alias("vote_average"),
    col("movie.vote_count").alias("vote_count"),
    col("movie.popularity").alias("popularity"),
    col("movie.genres").alias("genres"),
)

df = df.withColumn("genres", expr("transform(genres, x -> x.name)"))

# Convert back to DynamicFrame for AWS Glue write
df_output = DynamicFrame.fromDF(df, glueContext, "output_dynamic_frame")

# Writing the processed data to Parquet
glueContext.write_dynamic_frame.from_options(
    frame = df_output,
    connection_type = "s3",
    connection_options = {"path": OUTPUT_PATH+f"TMDB/{date.year}/{date.month}/{date.day}/details/"},
    format = "parquet"
)

print("Parquet file with details created")

input_dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3", 
    connection_options={"paths": [INPUT_PATH+"movies/"]}, 
    format="json", 
    format_options={"multiline": True}
)

df = input_dynamic_frame.toDF()
print("Dataframe Imported")

# All Jsons Merged
df = df.select(explode(col("results")).alias("movie"))

df = df.select(
    col("movie.id").alias("id"),
    col("movie.overview").alias("overview"),
    col("movie.popularity").alias("popularity"),
    col("movie.title").alias("title"),
    col("movie.vote_count").alias("vote_count"),
    col("movie.vote_average").alias("vote_average"),
    col("movie.release_date").alias("release_date"),
)

df_output = DynamicFrame.fromDF(df, glueContext, "output_dynamic_frame")

glueContext.write_dynamic_frame.from_options(
    frame = df_output,
    connection_type = "s3",
    connection_options = {"path": OUTPUT_PATH+f"TMDB/{date.year}/{date.month}/{date.day}/movies/"},
    format = "parquet"
)

print("Parquet file created with all movies")

job.commit()