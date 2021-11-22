import pandas as pd
import os
import json
from datetime import datetime
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

class loader_interface(object):
    ''' Load Data and setup interface for operation '''
    def __init__(self):
        # Conecting to Database
        #fb_key_path = os.getenv('FIREBASE_KEY_PATH')
        cred  = credentials.Certificate(f'./keys/key.json')
        app = firebase_admin.initialize_app(cred)

        db = firestore.client()
        self.pa_clc = db.collection(u'predicted_audience')
            
    def get_sample(self, prg_code, signal, date):
        try:
            return self.pa_clc.where(u'signal',u'==',signal).where(u'program_code', u'==', prg_code).where(u'date',u'==', date).get()
        except:
            raise Exception('An error occured while fetching PRG data')
    

    def get_sample_onRange(self, prg_code, signal, date1, date2):
        try:
            return self.pa_clc.where(u'signal',u'==',signal).where(u'program_code', u'==', prg_code).where(u'date',u'<=', date2).where(u'date', u'>=', date1).get()
        except:
            raise Exception('An error occured while fetching PRD data')
