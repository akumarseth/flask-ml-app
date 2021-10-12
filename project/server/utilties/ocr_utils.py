import pytesseract
from pdf2image import convert_from_path
import glob
import pathlib
import os
from project.server.app import app


app.config.from_pyfile('config.py')
tesseract_installtion_path = app.config['TESSERACT_PATH']


class ocr_utils:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        # self.pages = convert_from_path(
        #     pdf_path, poppler_path="C:\\python_env\\poppler-0.68.0_x86\\poppler-0.68.0\\bin")


    def get_pdf_text(self, start_page_no, end_page_no):
        pytesseract.pytesseract.tesseract_cmd = tesseract_installtion_path
        pages = convert_from_path(self.pdf_path, poppler_path="C:/python_env/poppler-0.68.0_x86/poppler-0.68.0/bin")

        all_data = [];
        for page_num, imgBlob in enumerate(pages):
            if page_num >= start_page_no and page_num <= end_page_no:
                text = pytesseract.image_to_string(imgBlob, lang='eng')
                data_with_page = (page_num, text)
                all_data.append(data_with_page)

        return all_data
