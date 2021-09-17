import spacy
import re
from spacy.lang.en.stop_words import STOP_WORDS
from pathlib import Path
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from collections import Counter
import os
import pandas as pd
import numpy as np


nlp = spacy.load('en_core_web_sm')


def getEntities(text):
    doc = nlp(text)
    result = []
    
    for ent in doc.ents:
        result.append(ent.text + ":" + ent.label_)
    
    return result


def sentence_segmentaion(file_content):

    file_content = file_content.replace("\n", "")

    # Create list of word tokens after removing stopwords

    text_sentences = nlp(file_content)
    sents_list = []
    for sentence in text_sentences.sents:
        sentence = str(sentence.text).replace("\n", "").replace("\t", " ")
        sents_list.append(sentence)

    return sents_list


def create_phrase_matcher(matacher_dict_list):
    matcher = PhraseMatcher(nlp.vocab)

    for matacher_dict in matacher_dict_list:
        # for key, val in matacher_dict:
        matcher_name = matacher_dict['feature_name']
        temp_list = [nlp(text) for text in matacher_dict['searchterm_set_list']]

        matcher.add("'"+matcher_name+"'", None, *temp_list)

    return matcher



def spacy_matcher_by_sent(listItem, matacher_dict):

    matcher = create_phrase_matcher(matacher_dict)
    result_classes = []
    nonlisted_issues = []
    listed_issues_by_sent = []
    
    for i in range(len(listItem)):
        doc = nlp(listItem[i])
        matches = matcher(doc)

        matchflag = 0
        for match_id, start, end in matches:
            # get the unicode ID, i.e. 'COLOR'
            rule_id = nlp.vocab.strings[match_id]
            span = doc[start: end]  # get the matched slice of the doc
            result_classes.append(rule_id.lower())
            matchflag = 1

        if matchflag == 1:
            listed_issues_by_sent.append(rule_id+" : "+listItem[i])

        # return confirmed_issues, probability_issues, nonlisted_issues, listed_issues
    return listed_issues_by_sent