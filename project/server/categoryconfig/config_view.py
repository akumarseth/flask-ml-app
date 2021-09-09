
from flask import Blueprint, request, redirect, make_response, jsonify

from project.server.auth.views import auth_required
from project.server.app import app, db
from project.server.dbmodel.documentmodel import Dcoument, Category, DocumentSchema

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.storage.blob import generate_blob_sas, AccountSasPermissions
from werkzeug.utils import secure_filename
import datetime
from datetime import datetime, timedelta
import string, random, requests
import os
import json
from marshmallow import ValidationError


config_blueprint = Blueprint('config', __name__)


app.config.from_pyfile('config.py')
account = app.config['STORAGE_ACCOUNT_NAME']   # Azure account name
key = app.config['ACCOUNT_KEY']      # Azure Storage account access key  
connect_str = app.config['CONNECTION_STRING']
container_name = app.config['CONFIG_CONTAINER_NAME'] # Container name

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container = ContainerClient.from_connection_string(connect_str, container_name)


def create_container_if_not_exist():
    try:
        container_properties = container.get_container_properties()
        # Container exists. You can now use it.
    except Exception as e:
        # Container does not exist. You can now create it.
        container_client = blob_service_client.create_container(container_name)



# @auth_required
def upload_config(category):
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            display_file_name = filename
            now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
            filename = now + '__' + filename
            
            file.save(filename)

            create_container_if_not_exist()

            blob_client = blob_service_client.get_blob_client(container = container_name, blob = filename)
            msg = ''
            with open(filename, "rb") as data:
                try:
                    blob_client.upload_blob(data, overwrite=True)
                    msg = "Upload Done ! "
                    # documentId = update_documentdetails_to_db(display_file_name, filename, category)
                    # if documentId is not None:
                    #     msg = "Upload Done ! "
                    # else:
                    #     msg = "upload fail"
                except Exception as e:
                    print(e)
            os.remove(filename)

            return msg

# add Rules for API Endpoints
config_blueprint.add_url_rule('/uploadconfig', view_func=upload_config, methods=['POST'])