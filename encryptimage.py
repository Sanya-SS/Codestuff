import cv2
import os
import pickle
import nacl.secret
import nacl.utils
from google.cloud import storage
#generate the encryption key 
def generate_key():
    key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
    with open('secret.bin','wb') as f:
        f.write(key)
    return key

#take image as input from user
file = input("Image Path: ")
if os.path.exists(file):
    img = cv2.imread(file)
else: 
    print("File not found")

#display image
cv2.imshow("Original image",img)
cv2.waitKey(0)
#encrypt the image
pickled_img = pickle.dumps(img)
key = generate_key()
box = nacl.secret.SecretBox(key)
encr = box.encrypt(pickled_img)

with open('img.bin','wb') as f:
    f.write(encr)

#uploading img.bin to gcp
bucket_name = 'name of bucket'
destination_blob_name = 'image.bin'
source_file_name = r"C:\Users\Sanya\projects\5\img.bin"

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)

blob.upload_from_filename(source_file_name)

print(f"File {source_file_name} uploaded to {destination_blob_name}.")