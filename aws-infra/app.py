import aws_cdk as cdk
from aws_cdk_infrastructure.hackmt_s3_bucket import HackMTBucket

app = cdk.App()
HackMTBucket(app, "hack-mt-bucket")

app.synth()
