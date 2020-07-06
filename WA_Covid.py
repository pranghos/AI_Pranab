# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 15:48:18 2020

@author: PRANABGHOSH
"""

import os
import sys
import configparser
import subprocess
import json
from argparse import ArgumentParser
import csv
import pandas as pd
from ibm_watson import AssistantV1
from ibm_watson import NaturalLanguageClassifierV1 
from ibm_watson import DiscoveryV1
from ibm_watson import NaturalLanguageUnderstandingV1
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, EntitiesOptions, KeywordsOptions


# Discovery
apikey = "TkQ4fyTXQgrc0lCBBGkX8j-QSZgBOB8_Gn7PG2_Nb1pG"
url = "https://api.eu-de.discovery.watson.cloud.ibm.com/instances/3ebf8d3f-6ef1-4997-a8ae-6ca089d5458f"

authenticator = IAMAuthenticator(apikey)
discovery = DiscoveryV1(
    version='2020-07-02',
    authenticator=authenticator
)

discovery.set_service_url('https://api.us-east.discovery.watson.cloud.ibm.com')
discovery.set_disable_ssl_verification(True)

env = discovery.list_environments
type(env)


# NLU
authenticator = IAMAuthenticator('G0-uQQFdYKp7SU0jPuhVf2NL7gcn93ggr-MRyMT31Rmj')

natural_language_understanding = NaturalLanguageUnderstandingV1( 
                version = '2019-07-12',
                authenticator = authenticator)

natural_language_understanding.set_service_url('https://api.eu-de.assistant.watson.cloud.ibm.com/instances/1c9f2201-10eb-4932-b26c-38337efbdddd')
natural_language_understanding.set_disable_ssl_verification(True)


response = natural_language_understanding.analyze(
    text='IBM is an American multinational technology company '
    'headquartered in Armonk, New York, United States, '
    'with operations in over 170 countries.',
    features=Features(
        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2)
       )).get_result()

print(json.dumps(response, indent=2))


type(response)

print(json.dumps(response, indent=2))


print(json.dumps(response, indent=2))

print(response.EntitiesOptions)
