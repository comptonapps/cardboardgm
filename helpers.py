from constants import S3, AWS_BUCKET
from PIL import Image
from models import Card
import io

THUMB_SIZE = (150, 150)


class ImageUploadException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def handle_image_upload(img_data, key_stub):
    thumb_img_key = upload_image(img_data, key_stub)
    return thumb_img_key

def upload_image(img_data, key_stub):
    print(f'\n\nUPLOADING\n\n')
    img_bytes = io.BytesIO()
    img_data.save(img_bytes, format=img_data.format)
    file_key = f"{key_stub}.{img_data.format}"
    response = S3.put_object(Body=img_bytes.getvalue(), Bucket=AWS_BUCKET, Key=file_key, ACL='public-read')
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise ImageUploadException("Error uploading photo to network")
    return file_key

def delete_record_from_s3(card):
    full_file_key = card.img_url
    thumb_file_key = full_file_key.replace("_full", "_thumb")
    remove_from_bucket(full_file_key)
    remove_from_bucket(thumb_file_key)

def remove_from_bucket(key):
    S3.delete_object(Bucket=AWS_BUCKET, Key=key)




