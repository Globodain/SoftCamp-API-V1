from google.cloud import storage
from google.oauth2 import service_account
from libraries.google_cloud.buckets import Buckets

credentials = service_account.Credentials.from_service_account_file('client.json')
storage_client = storage.Client(credentials=credentials)

class Functions:
    # Instance: Testing (development,testing) or Public (real) buckets
    
    def get_image(business_id: str, instance: str, image_name: str, public: bool):
        bucket = Buckets.get_bucket_url(False, public, instance)
        image = "{}/{}/{}".format(bucket,business_id,image_name)
        return image
    
    def get_folder_size(business_location: str, instance: str, folder_name: str, public: bool):
        bucket = Buckets.get_bucket_name(business_location, instance)
        blobs = storage_client.list_blobs(bucket, prefix=folder_name)
        bytes_used = sum([blob.size for blob in blobs])
        gigabytes_used = bytes_used / 1073741824  # Correct conversion from bytes to gigabytes
        print(f"{bucket} is using {gigabytes_used:0.3f} GB.")
        return f"{gigabytes_used:0.3f}"
    
    def create_folder(business_location: str, instance: str, folder_name: str):
        bucket = storage_client.get_bucket(Buckets.get_bucket_url(business_location, instance))
        blob = bucket.blob(folder_name + '/')
        blob.upload_from_string('')
        return 'Carpeta creada con éxito', 200

    def upload_file(business_location: str, instance: str, file: object, folder_name: str, filename: str, public: bool):
        get_bucket = Buckets.get_bucket_name(business_location, instance)
        bucket = storage_client.get_bucket(get_bucket)
        blob = bucket.blob(str(folder_name) + '/' + str(filename))
        blob.upload_from_file(file)

        if public:
            blob.make_public()
        else:
            blob.make_private()

        return 'Archivo subido con éxito', 200
    
    def list_folder_objects(business_location: str, instance: str, folder_name: str):
        bucket = Buckets.get_bucket_name(business_location, instance)
        blobs = storage_client.list_blobs(bucket, prefix=folder_name)
        
        objects = []
        for blob in blobs:
            blob.name = str(blob.name).replace(str(folder_name)+'/', '')
            objects.append(blob)
        
        return objects

    
    def delete_folder(business_location: str, instance: str, folder_name: str):
        """Elimina una carpeta del bucket de Google Cloud Storage"""
        bucket_name = Buckets.get_bucket_name(business_location, instance)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(f'{folder_name}')
        blob.delete()
    
    def delete_file(business_location: str, instance: str, folder_name: str, filename: str):
        """Elimina un archivo del bucket de Google Cloud Storage"""
        bucket_name = Buckets.get_bucket_name(business_location, instance)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(f'{folder_name}/{filename}')
        blob.delete()