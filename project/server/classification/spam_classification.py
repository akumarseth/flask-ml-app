from flask import Blueprint, request, redirect, make_response, jsonify, Response

from project.server.auth.views import auth_required
from project.server.app import app, db
from project.server.dbmodel.configmodel import *

from datetime import datetime, timedelta
import json
import pandas as pd
import numpy as np
import os

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from spacy.lang.en.stop_words import STOP_WORDS

from project.ml_model import *

import pickle
from sklearn.feature_extraction.text import CountVectorizer


spam_blueprint = Blueprint('spam', __name__)


def predict_using_countvector():
    try:

        post_text_data = request.get_json()
        text_to_predict = post_text_data.get("text_to_predict"),

        cwd = os.getcwd()
        ml_model_dir = os.path.join(cwd, 'project', 'ml_model','spam_countvectorizer')
        # load saved train model
        NB_spam_model = open(os.path.join(
            ml_model_dir, 'NB_countvector_spam_model.pickel'), 'rb')
        clf = pickle.load(NB_spam_model)

        # load saved vector
        vectorizer = open(os.path.join(
            ml_model_dir, 'NB_countvector_spam_vector.pickel'), "rb")
        cv = pickle.load(vectorizer)

        # text_to_predict = [text_to_predict]
        vect = cv.transform(text_to_predict).toarray()
        my_prediction = clf.predict(vect)
        print(my_prediction)

        return {'data': list(my_prediction)}

    except Exception as ex:
        print(ex)



def predict_using_BERT():
    try:
        pass

    except Exception as ex:
        print(ex)


# add Rules for API Endpoints
spam_blueprint.add_url_rule(
    '/spampredictioncountvector', view_func=predict_using_countvector, methods=['POST'])

spam_blueprint.add_url_rule(
    '/spampredictionbert', view_func=predict_using_BERT, methods=['GET'])
