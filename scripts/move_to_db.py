try:
    import firebase_admin
    import google.cloud
    from firebase_admin import credentials, firestore
    import pandas as pd
    import json
    import os
    from datetime import datetime
    import sys
    from google.cloud import storage
    import google.cloud.storage
    import io
    from io import BytesIO
    from google.cloud.firestore_v1.field_path import FieldPath
except Exception as e:
    print( "An Error Ocorred Importing librarys: {} ".format(e))


def _get_last_4_median(signal, prg_code, weekday):
            return au_df[(au_df.signal == signal) &
                            (au_df.program_code == prg_code)&
                            (au_df.weekday == weekday)].sort_values(by='start_time').tail(4).average_audience.median()

class RepeatedMigration(Exception):
    pass

# Initialize Cloud Storage DB
print('- Setting up GOOGLE CLOUD STORE')
cs_key_path = os.getenv('CLOUD_STORE_KEY_PATH')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cs_key_path
storage_client = storage.Client('GOOGLE_APPLICATION_CREDENTIALS')
bucket = storage_client.get_bucket('dgb-csv-store')


# Initialize Firestore DB
print('- Setting up FIRESTORE')
fb_key_path = os.getenv('FIREBASE_KEY_PATH')
cred  = credentials.Certificate(fb_key_path)
app = firebase_admin.initialize_app(cred)

db = firestore.client()
pa_clc = db.collection(u'predicted_audience')
av_clc = db.collection(u'inventory_availability')
au_clc = db.collection(u'program_audience')

mig_clc = db.collection(u'migration_history')


# Check Migration Availability
try:
    last_mig = mig_clc.order_by(u'creation_timestamp').limit(1).get()[0]
    if last_mig.to_dict()['creation_timestamp'].date() == datetime.today().date():
        raise RepeatedMigration
except RepeatedMigration:
    print('!! WARNING !!: [Migration Already on DB for {} date]'.format(datetime.today().date()))
    sys.exit(1)
except:
    pass

#Import Data
print('- Importing Data')
av_file_name = 'tvaberta_inventory_availability_v2.csv'
au_file_name = 'tvaberta_program_audience_v2.csv'
av_df = pd.read_csv(
        io.BytesIO(
                bucket.blob(blob_name = av_file_name).download_as_string()
                ) ,
                    encoding='UTF-8',
                    sep=';')

au_df = pd.read_csv(
        io.BytesIO(
                bucket.blob(blob_name = au_file_name ).download_as_string()
                ) ,
                    encoding='UTF-8',
                    sep=',')


print('- Prepering Data')
#Convert dates from strings to operable datetime objects
start_time = lambda x: datetime.fromisoformat(x[:-1])
weekday_f1 = lambda x: datetime.strptime(x, '%Y-%m-%d').weekday()
weekday_f2 = lambda x : datetime.strptime(x, '%d/%m/%Y').weekday()

au_df['start_time'] = au_df['program_start_time'].apply( start_time )
au_df['weekday'] = au_df['exhibition_date'].apply( weekday_f1 )
av_df['weekday'] = av_df['date'].apply( weekday_f2 )

       
#Apply median to av_DF
pa_df = av_df
pa_df['predicted_audience'] = av_df.apply(lambda row: _get_last_4_median(row['signal'],row['program_code'],row['weekday']), axis=1)
pa_df['date'] = pa_df.date.apply( lambda date : datetime.strptime(date, '%d/%m/%Y') )

#Adding Date Migration Obj


print("-- au_df:", au_df.shape)
print("-- av_df:", av_df.shape) 
print("-- pa_df:", pa_df.shape)

'''
# Delete Data
print("- Cleaning Database")
try:
    for _clc in [pa_clc,av_clc,au_clc]:
        docs = _clc.stream()
        [doc.reference.delete() for doc in docs]

except Exception as e:
    print(u'An Error Ocurred Cleaning Db: {e}')
'''

# Add Data
print("- Adding New Data")

## - Setup date_obj as a time reference for migration and documents timestamp
date_obj = datetime.now()

try:
    tmp = pa_df.to_dict(orient='records')
    doc_ref_list = list(map(lambda x: pa_clc.add(x), tmp))
    pa_id_list = [ doc[1].id for doc in doc_ref_list ]
     
    tmp = au_df.to_dict(orient='records')
    doc_ref_list = list(map(lambda x: av_clc.add(x), tmp)) 
    av_id_list = [ doc[1].id for doc in doc_ref_list ]
    
    tmp = av_df.to_dict(orient='records')
    doc_ref_list = list(map(lambda x: au_clc.add(x), tmp))
    au_id_list = [ doc[1].id for doc in doc_ref_list ]
    
except Exception as e:
    print( f'An Error Ocurred Adding Data: {e}')

# Add Migration Info
print("- Register Migration History")
try:
    
    mig_data = {
        u'audience_file_name':      au_file_name,
        u'availability_file_name':  av_file_name,
        u'audience_size':       len(au_df),
        u'availability_size':   len(av_df),
        u'predicted_size':      len(pa_df),
        u'pa_id': pa_id_list,
        u'au_id': au_id_list,
        u'av_id': av_id_list,
        u'creation_timestamp':  date_obj
            }
    
    mig_clc.document(date_obj.strftime('%d-%m-%Y')).set(mig_data)
except Exception as e:
    print(u'An Error Ocurred on Migration History Register: {e}')


# Check if Data Stored
print("- Checking Data Consistency")
try:
        pa_chk = [ pa_clc.document(_id).get() for _id in pa_id_list]
        assert pa_chk != None
        assert len(pa_chk) == len(pa_id_list)

        av_chk = [ av_clc.document(_id).get() for _id in av_id_list]
        assert av_chk != None
        assert len(av_chk) == len(av_id_list)
        
        au_chk = [ au_clc.document(_id).get() for _id in au_id_list]
        assert au_chk != None
        assert len(au_chk) == len(au_id_list)


        '''
        for doc in docs:
            print(u'Doc Data:{}'.format(doc.to_dict()))
        '''
except google.cloud.exceptions.NotFound:
    print(u'No Data Found')
except Exception as e:
    print(u'An Error Ocurred on Data Consistency Check: {e}')

print('DATABASE UPDATE SUCCESSFULL')
