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
import numpy as np
from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import ibm_db
from ibm_db import connect
import ibm_db_dbi
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import sys

def conn_db():
   
  conn = connect('DATABASE=BLUDB;'
                     'HOSTNAME=dashdb-txn-sbox-yp-dal09-11.services.dal.bluemix.net;'
                     'PORT=50000;'
                     'PROTOCOL=TCPIP;'
                     'UID=dnr61151;'
                     'PWD=1l2mz7b+hclkfnj0;', '', '')
  
  sql = 'select * from COVIDFAQ LIMIT 5;'
  #cur = ibm_db.exec_immediate(conn,sql)
  cur = ibm_db_dbi.Connection(conn)
  df = pd.read_sql(sql, cur)
  #result = ibm_db.fetch_assoc(cur)
  #df = pd.DataFrame(result, index=[0])
  #df = pd.DataFrame.from_dict(result, index=[0])
  return df

def getData():
  in_file = 'C:/McD/covid/Covid_FAQ_v2.xlsx'
  sheet_tab_all = 'Sheet1'
  #sheet_tab_ut_to_intent = 'Utterances to intents'
  #sheet_tab_entities = 'Entities'
 
  xls_in = pd.ExcelFile(in_file)
  df_all = pd.read_excel(xls_in, sheet_tab_all)
  #df_ut = pd.read_excel(xls_in, sheet_tab_ut_to_intent)
  #df_ent = pd.read_excel(xls_in, sheet_tab_entities)
  #df_all.shape
  #df_ent.head()
  df_int_s = df_all['Intent'] #intents
  df_int = df_int_s.to_frame()

  df_q_s = df_all['IntentExamples'] # questions
  df_q = df_q_s.to_frame()
  
  df_ent_s = df_all['Entities'] # Entities
  df_ent = df_ent_s.to_frame()
  
  df_entval_s = df_all['EntityValues'] # Entity values
  df_entval = df_entval_s.to_frame()
  
    
  return df_int, df_q, df_ent, df_entval


def wa_api_conn():
    
    authenticator = IAMAuthenticator('o76JGGNsgDZA1b7dyvWO1EOAlyONV3jEzr48H_C9nnAQ')
    assistant = AssistantV1(
            version='2020-04-01',
            authenticator=authenticator
            )
    assistant.set_service_url('https://api.eu-de.assistant.watson.cloud.ibm.com')
    return assistant 
    
#CREATE WORKSPACE & GET THE WORKSPACE ID
def create_workspace(assistant):
    resp = assistant.create_workspace(name='UC2AutoBot_test2',description='UC2 test 2').get_result()
    workspace_id = resp['workspace_id']
    return workspace_id

    
    examples = []
    while result:    
        examples.append({'text':result['INTENTS']})
        result = ibm_db.fetch_assoc(cur)
       
    resp = assistant.create_intent(workspace_id=workspace_id, intent = 'test_2', examples = examples).get_result()  
    return resp

def main():
  print("\nBegin automation \n")
  
  print("\nConnectiing to DB \n")
  df = conn_db() 
  print(type(df))
  print(df)
  
  
  print("\nGetting data from excel sheet \n")
  wa_Data = getData()  
  print(wa_Data)
  
  print("\nconnect to WA thourgh API \n")
  assistant = wa_api_conn()
  
  print("\ncreate workspace \n")
  workspace_id=create_workspace(assistant)
  print(workspace_id)

  
  print("\nGet Intents and Entity \n")
  df_int, df_q, df_ent, df_entval = getData()
  
  
  
  df_int_dict = df_int.to_dict()
  df_q_dict = df_q.to_dict()
  df_ent_dict = df_ent.to_dict() 
  df_entval_dict = df_entval.to_dict() 
  
  examples = []
  while df_q_dict:    
      examples.append({'text':df_q_dict['IntentExamples']})
      result = ibm_db.fetch_assoc(cur)
  
  resp = assistant.create_intent(workspace_id=workspace_id, intent = 'Define', examples = examples).get_result()
  '''
 
if __name__ == "__main__":

  main()

  
# end script





