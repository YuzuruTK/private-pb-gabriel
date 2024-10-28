import sys
from datetime import date
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import year, month, dayofmonth, col, quarter
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

# Constants
date = date.today()
# INPUT_PATH = f"s3://data-lake-do-gabriel-buron/TRUSTED/TMDB/{date.year}/{date.month}/{date.day}/"
INPUT_PATH = "s3://data-lake-do-gabriel-buron/TRUSTED/TMDB/2024/10/28/"
OUTPUT_PATH = "s3://data-lake-do-gabriel-buron/REFINED/"

# Glue Settings
glueContext = GlueContext(SparkContext())
spark = glueContext.spark_session
job = Job(glueContext)
job.init('movies_keywords_merge', {})

# Reading Json
movies_dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [INPUT_PATH+"movies/"]},
    format="parquet", 
    format_options={"multiline": True}
)
print("Dataframe Imported")

df_movies = movies_dynamic_frame.toDF()


df_time = df_movies.select(
    col("release_date").alias("id"),
    year(col("release_date")).alias("year"),
    month(col("release_date")).alias("month"),
    dayofmonth(col("release_date")).alias("day"),
    quarter(col("release_date")).alias("quarter"),
)

# merged_df = df_movies.join(df_keywords, on="id", how="left")

df_output = DynamicFrame.fromDF(df_movies, glueContext, "output_dynamic_frame")

# Writing the processed data to Parquet
glueContext.write_dynamic_frame.from_options(
    frame = df_output,
    connection_type = "s3",
    connection_options = {"path": OUTPUT_PATH+"FACT_movies/"},
    format = "parquet"
)

df_output = DynamicFrame.fromDF(df_time, glueContext, "output_dynamic_frame")

# Writing the processed data to Parquet
glueContext.write_dynamic_frame.from_options(
    frame = df_output,
    connection_type = "s3",
    connection_options = {"path": OUTPUT_PATH+"DIM_time/"},
    format = "parquet"
)

print("Parquet file with merged movies and keywords")

job.commit()