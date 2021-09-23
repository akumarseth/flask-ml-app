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


news_blueprint = Blueprint('news', __name__)


def classify_using_CNN():
    try:

        post_text_data = request.get_json()
        text_to_predict = post_text_data.get("text_to_predict"),

        cwd = os.getcwd()
        ml_model_dir = os.path.join(cwd, 'project', 'ml_model', 'news_classification', 'cnn')

        max_length = 200

        tokenizer = pickle.load(open(os.path.join(ml_model_dir,'news_classification_model_CNN_tokenizer'),'rb'))
        model = tf.keras.models.load_model(os.path.join(ml_model_dir, 'news_classification_model_CNN'))


        seq = tokenizer.texts_to_sequences(text_to_predict)
        padded = pad_sequences(seq, maxlen=max_length)
        pred = model.predict(padded)
        labels = ['sport', 'bussiness', 'politics', 'tech', 'entertainment']
        print(pred, labels[np.argmax(pred)])

        return {'data':labels[np.argmax(pred)]}

    except Exception as ex:
        print(ex)



def classify_using_LSTM():
    try:

        post_text_data = request.get_json()
        text_to_predict = post_text_data.get("text_to_predict"),

        cwd = os.getcwd()
        ml_model_dir = os.path.join(cwd, 'project', 'ml_model', 'news_classification', 'lstm')

        max_length = 200

        tokenizer = pickle.load(open(os.path.join(ml_model_dir,'news_classification_model_LSTM_tokenizer'),'rb'))
        model = tf.keras.models.load_model(os.path.join(ml_model_dir, 'news_classification_model_LSTM'))


        seq = tokenizer.texts_to_sequences(text_to_predict)
        padded = pad_sequences(seq, maxlen=max_length)
        pred = model.predict(padded)
        labels = ['sport', 'bussiness', 'politics', 'tech', 'entertainment']
        print(pred, labels[np.argmax(pred)])

        return {'data':labels[np.argmax(pred)]}

    except Exception as ex:
        print(ex)



def classify_using_BERT():
    try:
        pass

    except Exception as ex:
        print(ex)


# add Rules for API Endpoints
news_blueprint.add_url_rule(
    '/classifycnn', view_func=classify_using_CNN, methods=['POST'])

news_blueprint.add_url_rule(
    '/classifylstm', view_func=classify_using_LSTM, methods=['POST'])

news_blueprint.add_url_rule(
    '/classifybert', view_func=classify_using_BERT, methods=['POST'])