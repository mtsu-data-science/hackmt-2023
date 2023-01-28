import streamlit as st
import awswrangler as wr

s3_bucket_name = "data-science-club-hackmt-2023"

def example_func():
    st.write("Hello World!")

def write_subreddit_data_to_s3(df, subreddit_name, file_name):
    wr.s3.to_parquet(
        df=df,
        path=f"s3://{s3_bucket_name}/subreddit_data/{subreddit_name}/{file_name}.parquet",
        dataset=False,
    )

def read_subreddit_data_from_s3(subreddit_name, file_name):
    return wr.s3.read_parquet(
        path=f"s3://{s3_bucket_name}/subreddit_data/{subreddit_name}/{file_name}.parquet",
        dataset=False,
    )