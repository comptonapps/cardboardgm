from constants import S3, AWS_BUCKET, IMG_FORMAT, AVATAR_LARGE, AVATAR_THUMB, CARD_LARGE, CARD_THUMB
from PIL import Image
from models import Card, User
import io

class ImageUploadException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

# def handle_image_upload(img_data, key_stub):
#     thumb_img_key = upload_image(img_data, key_stub)
#     return thumb_img_key

# def upload_image(img_data, key_stub):
#     img_bytes = io.BytesIO()
#     img_data.save(img_bytes, format=img_data.format)
#     file_key = f"{key_stub}.{img_data.format}"
#     response = S3.put_object(Body=img_bytes.getvalue(), Bucket=AWS_BUCKET, Key=file_key, ACL='public-read')
#     
#     return file_key
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
    S3.put_object(Body=stream.getvalue(), Bucket=AWS_BUCKET, Key=key, ACL='public-read')
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise ImageUploadException("Error uploading photo to network")

def delete_record_from_s3(obj):
    S3.delete_object(Bucket=AWS_BUCKET, Key=obj.S3_large_key())
    S3.delete_object(Bucket=AWS_BUCKET, Key=obj.S3_thumb_key())

 






