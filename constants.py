import boto3
import os

aws_access_key = os.environ.get('AWS_ACCESS_KEY', "AKIAJXS3XJYIQMSMJZHA")
aws_secret_key = os.environ.get('AWS_SECRET_KEY', "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")

S3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
AWS_BUCKET = "cardboardgmpics"
AWS_URL = "https://cardboardgmpics.s3-us-west-2.amazonaws.com/"
EBAY_RESULT_COUNT = 50
EBAY_URL_ENDPOINT = f"https://svcs.ebay.com/services/search/FindingService/v1"
EARLIEST_YEAR = 1888
CURRENT_YEAR = 2020
API_LIMIT = 15
AVATAR_LARGE = (300, 300)
AVATAR_THUMB = (150, 150)
CARD_LARGE = (600, 600)
CARD_THUMB = (300, 300)
IMG_FORMAT = 'JPEG'
