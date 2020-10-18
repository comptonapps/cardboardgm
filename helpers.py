from constants import S3, AWS_BUCKET, IMG_FORMAT, AVATAR_LARGE, AVATAR_THUMB, CARD_LARGE, CARD_THUMB
from PIL import Image
from models import Card, User
import io

class ImageUploadException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def upload_img(img, obj):
    images = [img.copy(), img.copy()]
    for img in images:
        img.format = IMG_FORMAT
    large = AVATAR_LARGE
    thumb = AVATAR_THUMB
    if type(obj) == Card:
        large = CARD_LARGE
        thumb = CARD_THUMB
    images[0].thumbnail(large)
    images[1].thumbnail(thumb)
    large_key = obj.S3_large_key()
    thumb_key = obj.S3_thumb_key()
    upload_image_to_S3_bucket(images[0], large_key)
    upload_image_to_S3_bucket(images[1], thumb_key)

def upload_image_to_S3_bucket(img, key):
    stream = io.BytesIO()
    img.save(stream, format=IMG_FORMAT)
    response = S3.put_object(Body=stream.getvalue(), Bucket=AWS_BUCKET, Key=key, ACL='public-read')
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise ImageUploadException("Error uploading photo to network")

def delete_record_from_s3(obj):
    S3.delete_object(Bucket=AWS_BUCKET, Key=obj.S3_large_key())
    S3.delete_object(Bucket=AWS_BUCKET, Key=obj.S3_thumb_key())

 






