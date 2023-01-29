import streamlit as st
import awswrangler as wr

s3_bucket_name = "data-science-club-hackmt-2023"

# Backend - this is how you send data to s3
# open folder 
# for csv file in folder:
# run write_subreddit_data_to_s3 for each with all args = the title of the subreddit name
def write_subreddit_data_to_s3(df, subreddit_name, file_name):
    """write_subreddit_data_to_s3 writes a dataframe to s3 in a compressed
    file format that will optimize both storage and read times.

    We should land on standard file_names for each data file so it is consistent
    when accessing different subreddits.

    Args:
        df (Pandas DataFrame): DataFrame to be stored in S3
        subreddit_name (str): The name of the subreddit
        file_name (str): A distinct filename
    """

    wr.s3.to_parquet(
        df=df,
        path=f"s3://{s3_bucket_name}/subreddit_data/{subreddit_name.lower()}/{file_name}.parquet",
        dataset=False,
    )

# Frontend: this is how you get data FROM s3
def read_subreddit_data_from_s3(subreddit_name, file_name):
    """read_subreddit_data_from_s3 returns a dataframe stored in s3 for analysis

    Args:
        subreddit_name (str): The name of the subreddit
        file_name (str): A distinct filename

    Returns:
        Pandas DataFrame: The dataframe stored in s3
    """

    return wr.s3.read_parquet(
        path=f"s3://{s3_bucket_name}/subreddit_data/{subreddit_name}/{file_name}.parquet",
        dataset=False,
    )
