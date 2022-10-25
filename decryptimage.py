import cv2
import os
import pickle
import nacl.secret
import nacl.utils
from google.cloud import storage

#download image from gcp
bucket_name = 'name of bucket'
source_blob_name = 'image.bin'
destination_file_name = r"C:\Users\Sanya\projects\5"
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(source_blob_name)
blob.download_to_filename(destination_file_name)
print("Downloaded storage object {} from bucket {} to local file {}.".format(source_blob_name, bucket_name, destination_file_name))

#decrypt the image
def get_key():
    with open('secret.bin','rb') as f:
        key = f.read()
    return key

key = get_key()
box = nacl.secret.SecretBox(key)
with open('img.bin','rb') as f:
    data_from_file = f.read()
decrypted_data = box.decrypt(data_from_file)
img_decr = pickle.loads(decrypted_data)

cv2.imshow('decrypted',img_decr)
cv2.waitKey(0)
