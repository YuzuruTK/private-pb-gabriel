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
# INPUT_PATH = f"s3://data-lake-do-gabriel-buron/TRUSTED/TMDB/{date.year}/{date.month}/{date.day}/"
INPUT_PATH = "s3://data-lake-do-gabriel-buron/TRUSTED/TMDB/2024/10/28/"
OUTPUT_PATH = "s3://data-lake-do-gabriel-buron/REFINED/"

# Glue Settings
glueContext = GlueContext(SparkContext())
spark = glueContext.spark_session
job = Job(glueContext)
job.init('details import', {})

# Reading Json
details_dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3", 
    connection_options={"paths": [INPUT_PATH+"details/"]},
    format="parquet", 
    format_options={"multiline": True}
)

print("Dataframe Imported")

df = details_dynamic_frame.toDF()

df_output = DynamicFrame.fromDF(df, glueContext, "output_dynamic_frame")

# Writing the processed data to Parquet
glueContext.write_dynamic_frame.from_options(
    frame = df_output,
    connection_type = "s3",
    connection_options = {"path": OUTPUT_PATH+"DIM_details/"},
    format = "parquet"
)

print("Parquet file with details")

job.commit()