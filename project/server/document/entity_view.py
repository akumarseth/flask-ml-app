from project.server.dbmodel.documentmodel import Dcoument
from flask import Blueprint, request, redirect, make_response, jsonify
from project.server.auth.views import auth_required
from project.server.app import app, db
from project.server.utilties.nlp_utils import *
from project.server.utilties.base_utils import base_utils
from project.server.utilties.azure_utils import *

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.storage.blob import generate_blob_sas, AccountSasPermissions

from datetime import datetime, timedelta
import urllib
import numpy as np
import requests
from PyPDF2 import PdfFileReader
from flaskext.markdown import Markdown

entity_blueprint = Blueprint('entity_blueprint', __name__)

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

app.config.from_pyfile('config.py')
account = app.config['STORAGE_ACCOUNT_NAME']   # Azure account name
key = app.config['ACCOUNT_KEY']      # Azure Storage account access key
connect_str = app.config['CONNECTION_STRING']
container_name = app.config['CONTAINER_NAME']  # Container name

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container = ContainerClient.from_connection_string(connect_str, container_name)

Markdown(app)

def get_blob_details_from_db(doc_id):
    try:
        doc_detail = Dcoument.query.get(doc_id)
        if doc_detail:
            blob_name = doc_detail.file_name

        return blob_name
    except Exception as ex:
        print(ex)


def entity_extractor(doc_id):
    try:
        # config_details = get_config_data_from_db(category)
        blob_name = get_blob_details_from_db(doc_id)
        pdf_path = download_blob_and_save_to_local(blob_name)

        page_content = ''
        with open(pdf_path, 'rb') as f:
            pdf_reader = PdfFileReader(f)
            information = pdf_reader.getDocumentInfo()
            number_of_pages = pdf_reader.getNumPages()

            for page_number in range(10):
                page_obj = pdf_reader.getPage(page_number)
                page_content += page_obj.extractText()

        html = entity_view_displacy(page_content)
        result = HTML_WRAPPER.format(html)
        
        return {'pdf_content': page_content, 'data': result}
    except Exception as ex:
        print(ex)
    finally:
        os.remove(pdf_path)


entity_blueprint.add_url_rule(
    '/entity_view/<doc_id>', view_func=entity_extractor, methods=['GET'])
