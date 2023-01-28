from aws_cdk import Stack, aws_s3 as s3, App


class HackMTBucket(Stack):
    def __init__(self, app: App, id: str) -> None:
        super().__init__(app, id)

        # data buckets
        data_store_bucket_name = f"data-science-club-hackmt-2023"

        source_bucket = s3.Bucket(
            self,
            data_store_bucket_name,
            bucket_name=data_store_bucket_name,
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )
