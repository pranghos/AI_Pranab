# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 13:23:51 2020

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
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import ibm_db
from ibm_db import connect


#Create database connection
conn = connect('DATABASE=BLUDB;'
                     'HOSTNAME=dashdb-txn-sbox-yp-dal09-11.services.dal.bluemix.net;'
                     'PORT=50000;'
                     'PROTOCOL=TCPIP;'
                     'UID=dnr61151;'
                     'PWD=1l2mz7b+hclkfnj0;', '', '')


#Setting Authenticator & creating Assistant
authenticator = IAMAuthenticator('o76JGGNsgDZA1b7dyvWO1EOAlyONV3jEzr48H_C9nnAQ')
assistant = AssistantV1(
    version='2020-04-01',
    authenticator=authenticator
)
assistant.set_service_url('https://api.eu-de.assistant.watson.cloud.ibm.com')

#CREATE WORKSPACE & GET THE WORKSPACE ID
resp = assistant.create_workspace(name='UC2AutoBot_test2',description='UC2 test 2').get_result()
workspace_id = resp['workspace_id']
print(workspace_id)
type(workspace_id)

cursor = None
while True:
    response=assistant.list_examples(
        workspace_id='3d7911a4-f3cd-41d1-ae0c-cf043d076d13',
#        workspace_id= '7fcf65ee-268f-493f-b9bf-45c8b57def48',
        intent='Client_and_business_partner',
        cursor=cursor,
        page_limit=3
    ).get_result()

    for example in response.get('examples'):
        print(example.get('text'))

    cursor=response.get('pagination').get('next_cursor')
    if not cursor:
        break
    
#RETREIVING FIRST 2 UTTERANCES FROM DATABASE TO CREATE AN INTENT
stmt = 'select * from COVIDFAQ LIMIT 5;'
cur = ibm_db.exec_immediate(conn,stmt)
result = ibm_db.fetch_assoc(cur)
print(result)
examples = []
while result:    
    examples.append({'text':result['QUESTIONS']})
    result = ibm_db.fetch_assoc(cur)
    print(result)
resp = assistant.create_intent(workspace_id=workspace_id, intent = 'test_2', examples = examples).get_result()    