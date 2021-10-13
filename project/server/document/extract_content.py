from project.server.dbmodel.configmodel import ConfigTemplate,ConfigTemplateMetadata
from project.server.dbmodel.documentmodel import Dcoument
from flask import Blueprint, request, redirect, make_response, jsonify
from project.server.auth.views import auth_required
from project.server.app import app, db
from project.server.utilties.nlp_utils import *
from project.server.utilties.base_utils import base_utils
from project.server.utilties.azure_utils import *
from project.server.utilties.ocr_utils import ocr_utils

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.storage.blob import generate_blob_sas, AccountSasPermissions

from datetime import datetime, timedelta
import urllib
import numpy as np
import requests
from PyPDF2 import PdfFileReader


extract_blueprint = Blueprint('extract_blueprint', __name__)

app.config.from_pyfile('config.py')
account = app.config['STORAGE_ACCOUNT_NAME']   # Azure account name
key = app.config['ACCOUNT_KEY']      # Azure Storage account access key  
connect_str = app.config['CONNECTION_STRING']
container_name = app.config['CONTAINER_NAME'] # Container name

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container = ContainerClient.from_connection_string(connect_str, container_name)


def get_config_data_from_db(category):
    try:
        final_data = []

        template_details = ConfigTemplate.query.filter_by(category=category,is_default=True).first()
        if template_details is None:
            return make_response(f"No configuation found for the category {category}"), 401
        
        template_metadata = ConfigTemplateMetadata.query.filter_by(template_id=template_details.id).all()
        pattern_list = set()
        for config in template_metadata:
            pattern_list.add(config.feature_name)
        
        for pattern_name in pattern_list:
            dict_list = {
                            'feature_name':pattern_name,
                            'searchterm_set_list':tuple([x.pattern for x in template_metadata if x.feature_name == pattern_name])
                        }

            final_data.append(dict_list)

        return final_data
         
    except Exception as ex:
        print(ex)


def extract_basic_info_from_first_page(text):
    main_list = []
    pdf_first_page_result = text
    sentences = sentence_segmentaion(pdf_first_page_result.replace('\n', ''))

    contract_title = sentences[0]
    entities_first_sen = getEntities(sentences[1])

    agreement_date = ''
    supplier = ''

    for ent in entities_first_sen:
        if 'DATE' in ent:
            agreement_date = str(ent).split(':')[0]
            continue
        
        if 'ORG' in ent :
            if 'llc' in str(ent).lower(): # and entities_first_sen[-2] in str(ent).lower():
                supplier = str(ent).split(':')[0]
                break

    main_list.append({
        "Metadata heading": "Supplier",
        "Information Extracted":supplier,
        "Comments/Citation":"Page 1"
    })

    main_list.append({
        "Metadata heading": "Contract Type",
        "Information Extracted":"",
        "Comments/Citation":""
    })

    main_list.append({
        "Metadata heading": "Contract Title",
        "Information Extracted":contract_title,
        "Comments/Citation":"Page 1"
    })

    main_list.append({
        "Metadata heading": "Effective Date",
        "Information Extracted":agreement_date,
        "Comments/Citation":"Page 1"
    })

    main_list.append({
        "Metadata heading": "Agreement Type",
        "Information Extracted":contract_title,
        "Comments/Citation":"Page 1"
    })

    return main_list


def process_extract_data(matched_sentences, page_no):
    try:
        main_list = []
        ## read the pdf document
        for i in range(len(matched_sentences)):
            metadata_heading = ''
            information_extracted = []
            datetime_data = []
            commission = []
            res_money = []
            pages = []

            res_money_val =''
            commission_val = ''
            datetime_data_val = ''


            metadata_heading = matched_sentences[i].split(':')[0]
            info_val = matched_sentences[i].split(':')[1]

            entity_list = getEntities(matched_sentences[i])

            if entity_list != None:
                matched_res_money = [ent.split(':')[0] for ent in entity_list if 'MONEY' in ent]
                if matched_res_money != None: 
                    if len(matched_res_money) > 0:
                        res_money_val = matched_res_money[0]


            res = re.findall(r'\d+%', matched_sentences[i])
            if res:
                for ind in range(len(res)):
                    commission_val = res[ind]
                

            monthyear = base_utils().getMonthandYear(matched_sentences[i])
            if monthyear:

                for ind in range(len(monthyear)):
                    datetime_data_val = monthyear[ind]

            is_found = False
            for dict_data in main_list:
                for key in dict_data:
                    if dict_data["Metadata heading"] == metadata_heading:
                        is_found = True
                        dict_data["Information Extracted"].append(info_val),
                        dict_data["Information Extracted"] = list(set(dict_data["Information Extracted"]))

                        page_val = "Page " + str(page_no)
                        dict_data["Comments/Citation"].append(page_val)
                        dict_data["Comments/Citation"] = list(set(dict_data["Comments/Citation"]))

                        if commission_val:
                            dict_data["output 1"].append(commission_val)
                            dict_data["output 1"] = list(set(dict_data["output 1"]))
                        if res_money_val:
                            dict_data["output 2"].append(res_money_val)
                            dict_data["output 2"] = list(set(dict_data["output 2"]))
                        if datetime_data_val:
                            dict_data["output 3"].append(datetime_data_val)
                            dict_data["output 3"] = list(set(dict_data["output 3"]))
                
            if is_found == False:
                information_extracted.append(info_val)
                commission.append(commission_val)
                res_money.append(res_money_val)
                datetime_data.append(datetime_data_val)

                page_val = "Page " + str(page_no)
                pages.append(page_val)

                main_list.append({
                    "Metadata heading": metadata_heading,
                    "Information Extracted":information_extracted,
                    "Comments/Citation": list(set(pages)),
                    "output 1": list(set(commission)),
                    "output 2": list(set(res_money)),
                    "output 3": list(set(datetime_data))
                })

        return main_list
    
    except Exception as ex:
        print(ex)


# def download_blob_and_save_to_local(doc_id):
#     try:
#         blob_client = blob_service_client.get_blob_client(container = container_name, blob = "0266554465.jpeg")

#         # return blob_client.download_blob().readall()
#         doc_detail = Dcoument.query.get(doc_id)
#         if doc_detail:
#             blob_name = doc_detail.file_name
#             # print(blob_name)
#             url = f"https://{account}.blob.core.windows.net/{container_name}/{blob_name}"
#             sas_token = generate_blob_sas(
#                 account_name=account,
#                 account_key=key,
#                 container_name=container_name,
#                 blob_name=blob_name,
#                 permission=AccountSasPermissions(read=True),
#                 expiry=datetime.utcnow() + timedelta(hours=1)
#             )
#         url_with_sas = f"{url}?{sas_token}"

#         # req = urllib.urlopen(url_with_sas)
#         # return redirect(url_with_sas)

#         r = requests.get(url_with_sas, allow_redirects=True)
#         # filename = getFilename_fromCd(r.headers.get('content-disposition'))
#         open(blob_name, 'wb').write(r.content)
        
#         return blob_name
#     except Exception as ex:
#         print(ex)


def get_blob_details_from_db(doc_id):
    try:
        doc_detail = Dcoument.query.get(doc_id)
        if doc_detail:
            blob_name = doc_detail.file_name

        return blob_name
    except Exception as ex:
        print(ex)


def extract_sales_agreement(config_details,blob_name,pdf_path):
    
    with open(pdf_path, 'rb') as f:
        pdf_reader = PdfFileReader(f)
        information = pdf_reader.getDocumentInfo()
        number_of_pages = pdf_reader.getNumPages()

        final_extracted_data = []
        for page_number in range(10):
            page_obj = pdf_reader.getPage(page_number)
            page_content = page_obj.extractText()

            page_no = page_number + 1

            if page_number == 0:
                first_page_data = extract_basic_info_from_first_page(page_content)
                final_extracted_data.extend(first_page_data)

            sentence_list = sentence_segmentaion(page_content)
            matched_sentences = spacy_matcher_by_sent(sentence_list, config_details)
            main_list = process_extract_data(matched_sentences, page_no)
            final_extracted_data.extend(main_list)

            # extract_gainshare_of_guarnteed_productivity(page_content,page_no,file_name)
            # extract_Service_Request_acceptance_rejection_Service_level(page_content,page_no)
            
            # if 'Current Pricing'.lower() in page_content.lower():
            #     doc = nlputil.nlp_utilities.get_doc(page_content.replace('\n', ' '))
            #     # doc = nlputil.nlp_utilities.get_doc(page_content)
            #     for token in doc:
            #         if str(token.text).lower() == 'Current'.lower() or str(token.text).lower() == 'Current Pricing'.lower():
            #             index = token.i
            #             country = doc[index - 1]

            #     is_Table = extract_current_Pricing_if_table(page_no, pdf_path, result_excel_path,file_name,country, page_content)
            #     try:
            #         if is_Table == False:
            #             extract_Current_Pricing_if_not_table(page_content, page_no, pdf_path, result_excel_path,file_name,country)
            #     except:
            #         continue 
            
        # extract_Commencement_table(pdf_path, 167)
    
        # df = pd.DataFrame(final_extracted_data)
        # print(df)
        # df.to_excel("output.xlsx", sheet_name="Contract Metadata Output", index=False, engine='xlsxwriter')

    return {'count':len(final_extracted_data), 'data':final_extracted_data}


def process_financial_extracted_data(matched_sentences, page_no):
    extracted_list = []
    ## read the pdf document
    for i in range(len(matched_sentences)):
        metadata_heading = ''
        information_extracted = []
        entity = []
        pages = []
        res_entity_val = ''

        metadata_heading = matched_sentences[i].split(':')[0]
        info_val = matched_sentences[i].split(':')[1]

        entity_list = getEntities(matched_sentences[i])
        if entity_list != None:
            matched_res_money = [ent.split(':')[0] for ent in entity_list if 'MONEY' in ent]
            if matched_res_money != None: 
                if len(matched_res_money) > 0:
                    res_entity_val = matched_res_money[0]

        is_found = False
        for dict_data in extracted_list:
            for key in dict_data:
                if dict_data["Metadata heading"] == metadata_heading:
                    is_found = True
                    dict_data["Information Extracted"].append(info_val),
                    dict_data["Information Extracted"] = list(set(dict_data["Information Extracted"]))

                    # page_val = page_no
                    # dict_data["pages"].append(page_val)
                    # dict_data["pages"] = list(set(dict_data["pages"]))

                    if res_entity_val:
                        dict_data["entity"].append(res_entity_val)
                        dict_data["entity"] = list(set(dict_data["entity"]))
                    

        if is_found == False:
            information_extracted.append(info_val)
            entity.append(res_entity_val)
            pages.append(page_no)

            extracted_list.append({
                    "Metadata heading": metadata_heading,
                    "Information Extracted":information_extracted,
                    "Pages": list(set(pages)),
                    "Entity" :entity
                })

                        
    return extracted_list




def extract_financial_agreement(config_details,blob_name,pdf_path):
    ocr_util = ocr_utils(pdf_path)
    pdf_text_with_pageNum = ocr_util.get_pdf_text(5,15)

    final_data = []
    paragraph_data=[]
    text = []
    for page_text in pdf_text_with_pageNum:
        page_no=page_text[0];
        print("\n")
        print('**********************')
        print(page_no)
        print('**********************')
        print(page_no, page_text[1])
        sentence_list = page_text[1].split('\n');

        for line in sentence_list:
            text.append(line)
            entities = getEntities_new(line)
            for ent in entities:
                if ent[0] == 'MONEY' or ent[0] == 'CARDINAL':
                    text_to_display = line[:(len(line)-len(ent[1]))].strip()
                    data = {'page_no' : page_no, 'original_text':line,'text_to_display': text_to_display, 'entity':ent[1]}
                    final_data.append(data)

        matched_sentences = spacy_matcher_by_sent(text, config_details)
        paragraph_data.extend(process_financial_extracted_data(matched_sentences, page_no))
    return {'data':final_data, 'matched_data':paragraph_data}


def start_extracting(doc_id, category):
    try:
        config_details = get_config_data_from_db(category)
        blob_name = get_blob_details_from_db(doc_id)
        pdf_path = download_blob_and_save_to_local(blob_name)
        
        if category == 'Financial Agreement':
            return extract_financial_agreement(config_details,blob_name,pdf_path)
        else:
            return extract_sales_agreement(config_details,blob_name,pdf_path)
            
    except Exception as ex:
        print(ex)
    finally:
        os.remove(pdf_path)

        



# add Rules for API Endpoints
extract_blueprint.add_url_rule('/extract/<doc_id>/<category>', view_func=start_extracting, methods=['GET'])
