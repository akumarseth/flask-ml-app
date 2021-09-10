
from typing import final
from flask import Blueprint, request, redirect, make_response, jsonify, Response

from project.server.auth.views import auth_required
from project.server.app import app, db
from project.server.dbmodel.configmodel import *

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.storage.blob import generate_blob_sas, AccountSasPermissions
from werkzeug.utils import secure_filename
import datetime
from datetime import datetime, timedelta
import string
import random
import requests
import os
import json
from marshmallow import ValidationError
import pandas as pd


config_blueprint = Blueprint('config', __name__)


app.config.from_pyfile('config.py')
account = app.config['STORAGE_ACCOUNT_NAME']   # Azure account name
key = app.config['ACCOUNT_KEY']      # Azure Storage account access key
connect_str = app.config['CONNECTION_STRING']
container_name = app.config['CONFIG_CONTAINER_NAME']  # Container name

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container = ContainerClient.from_connection_string(connect_str, container_name)


def create_container_if_not_exist():
    try:
        container_properties = container.get_container_properties()
        # Container exists. You can now use it.
    except Exception as e:
        # Container does not exist. You can now create it.
        container_client = blob_service_client.create_container(container_name)


def update_template_details_to_db(display_template_name, template_name, catagory, template_version_no):
    """deactivate the current default template active - to make is_default = false"""
    existing_default_template_obj = ConfigTemplate.query.filter_by(
        is_default=True).first()
    if existing_default_template_obj: 
        existing_default_template_obj.is_default = 0
        db.session.add(existing_default_template_obj)
        db.session.commit()

    config_template_obj = ConfigTemplate(
        display_template_name=display_template_name,
        template_name=template_name,
        category=catagory,
        version_no=template_version_no,
        is_default=1,
        created_by="",
        created_date=datetime.now(),
        edited_by="",
        edited_date=datetime.now()
    )
    db.session.add(config_template_obj)
    db.session.commit()

    df = pd.read_excel(template_name, skiprows=2, engine='openpyxl')
    df1 = df.fillna(0)
    for i in df1.columns:
        template_featire_name = i

        patterns = list(df1[i])
        for pattern in patterns:
            if pattern != 0:
                config_template_metadata_obj = ConfigTemplateMetadata(
                    feature_name=template_featire_name,
                    pattern=pattern,
                    template_id=config_template_obj.id,
                    created_by="",
                    created_date=datetime.now(),
                    edited_by="",
                    edited_date=datetime.now()
                )
                db.session.add(config_template_metadata_obj)

    db.session.commit()
    return config_template_obj.id


# @auth_required
def upload_config(category):
    if request.method == 'POST':
        msg = ''

        try:
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                display_file_name = filename
                now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
                filename = now + '__' + filename

                file.save(filename)

                df = pd.read_excel(filename, engine='openpyxl',
                                header=None, usecols=[0, 1])
                df_1 = df[:2]
                template_version_no = str(list(df_1.loc[0])[1])
                template_category = list(df_1.loc[1])[1]

                """check if same version of template is availavle, if yes through eception else continue to upload"""
                config_template_obj = ConfigTemplate.query.filter_by(
                    version_no=template_version_no).first()
                if config_template_obj:
                    return Response(
                            response=f"Template with same version no. {template_version_no} is already available. Kindly upload config with latest version no.",
                            status=201
                        )

                if category != template_category:
                    return Response(
                            response=f"Template category is not same which you hve slected from dropdown.",
                            status=201
                        )

                create_container_if_not_exist()

                blob_client = blob_service_client.get_blob_client(
                    container=container_name, blob=filename)
                with open(filename, "rb") as data:
                    try:
                        blob_client.upload_blob(data, overwrite=True)
                        msg = "Upload Done ! "
                        documentId = update_template_details_to_db(
                            display_file_name, filename, category, template_version_no)
                        if documentId is not None:
                            msg = "Upload Done ! "
                        else:
                            msg = "upload fail"
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
            return Response(response=e.args, status=201)
        finally:
            os.remove(filename)

        return Response(response=msg, status=200)



def get_config_template_list(category):
    """get all config template by category"""
    try:
        config_template_list = ConfigTemplate.query.all()

        config_templatE_schema = ConfigTemplateSchema(many=True)
        results = config_templatE_schema.dump(config_template_list)
        return {"data": results}
    except Exception as e:
        print(e)
        return Response(
            response=e.args,
            status=201
        )


def get_config_template_metadata_by_template_id(template_id):
    """get config template metadata datails by template_id"""
    try:
        config_template_metadata_list = ConfigTemplateMetadata.query.filter_by(template_id=template_id).all()
        config_template_metadata_schema = ConfigTemplateMetadataSchema(many=True)
        results = config_template_metadata_schema.dump(config_template_metadata_list)
        return {"data": results}

    except Exception as e:
        print(e)
        return Response(response=e.args,status=201)


def get_config_template_details_by_category(category):
    try:
        config_template_metadata_details = ConfigTemplate.query\
            .join(ConfigTemplateMetadata, ConfigTemplate.id==ConfigTemplateMetadata.template_id)\
            .add_columns(ConfigTemplateMetadata.feature_name, ConfigTemplateMetadata.pattern)\
            .filter(ConfigTemplate.category == category)\
            .filter(ConfigTemplate.is_default == True).all()

        config_template_metadata_schema = ConfigTemplateMetadataSchema(many=True)
        results = config_template_metadata_schema.dump(config_template_metadata_details)
        return {"data": results}
    except Exception as e:
        print(e)
        return Response(response=e.args,status=201)



def update_config_template_to_default(template_id):
    try:
        need_to_make_default_template = ConfigTemplate.query.filter_by(id = template_id).first()
        if need_to_make_default_template is None:
            return Response(
                response="template is not found",
                status=401
            )
        

        """update existed default template to false"""
        existed_default_template = ConfigTemplate.query.filter_by(is_default=True).first()
        if existed_default_template:
            existed_default_template.is_default = 0
            existed_default_template.edited_by="",
            existed_default_template.edited_date=datetime.now()
            db.session.add(existed_default_template)
        
        
        need_to_make_default_template.is_default = 1
        need_to_make_default_template.edited_by="",
        need_to_make_default_template.edited_date=datetime.now()
        db.session.add(need_to_make_default_template)


        db.session.commit()

        return Response(
                response=f"template id {template_id} is set as default now",
                status=200
            )

    except Exception as e:
        print(e)
        return Response(response=e.args,status=201)


# add Rules for API Endpoints
config_blueprint.add_url_rule(
    '/uploadconfig/<category>', view_func=upload_config, methods=['POST'])

config_blueprint.add_url_rule(
    '/gettemplatelist/<category>', view_func=get_config_template_list, methods=['GET'])

config_blueprint.add_url_rule(
    '/gettemplatemetadata/<template_id>', view_func=get_config_template_metadata_by_template_id, methods=['GET'])

config_blueprint.add_url_rule(
    '/gettemplatedetails/<category>', view_func=get_config_template_details_by_category, methods=['GET'])

config_blueprint.add_url_rule(
    '/updatetemplatetodefault/<template_id>', view_func=update_config_template_to_default, methods=['PUT'])
