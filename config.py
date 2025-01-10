from dotenv import load_dotenv
import os

class BaseConfig():
    load_dotenv()

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_SECRET_ACCESS_KEY")
    API_KEY = os.getenv("API_KEY")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

conf = BaseConfig()