from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.storage.blob import generate_blob_sas, AccountSasPermissions

from datetime import datetime, timedelta
from project.server.app import app, db
import requests


app.config.from_pyfile('config.py')
account = app.config['STORAGE_ACCOUNT_NAME']   # Azure account name
key = app.config['ACCOUNT_KEY']      # Azure Storage account access key  
connect_str = app.config['CONNECTION_STRING']
container_name = app.config['CONTAINER_NAME'] # Container name

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container = ContainerClient.from_connection_string(connect_str, container_name)


def create_container_if_not_exist():
    try:
        container_properties = container.get_container_properties()
        # Container exists. You can now use it.
    except Exception as e:
        # Container does not exist. You can now create it.
        container_client = blob_service_client.create_container(container_name)


### NOT TESTED
def delete_contaiener_if_exist():
    try:
        container_properties = container.get_container_properties()
        # Container exists. You can now use it.
        container.delete_container()
    except Exception as e:
        # Container does not exist. You can now create it.
        container_client = blob_service_client.create_container(container_name)



def download_blob_and_save_to_local(blob_name):
    try:
        url = f"https://{account}.blob.core.windows.net/{container_name}/{blob_name}"
        sas_token = generate_blob_sas(
            account_name=account,
            account_key=key,
            container_name=container_name,
            blob_name=blob_name,
            permission=AccountSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        url_with_sas = f"{url}?{sas_token}"

        # req = urllib.urlopen(url_with_sas)
        # return redirect(url_with_sas)

        r = requests.get(url_with_sas, allow_redirects=True)
        # filename = getFilename_fromCd(r.headers.get('content-disposition'))
        open(blob_name, 'wb').write(r.content)
        
        return blob_name
    except Exception as ex:
        print(ex)

