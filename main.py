#Required Imports
import os
from flask import Flask, render_template, request, jsonify
from controller import controller as data_controller
import json
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime 


# Initialize Flask App
app = Flask(__name__)

# Routes
@app.route("/", methods=["GET"])
def homepage():
    try:
        status = 200
        response = jsonify('Audience Prediction REST API')
        return response,status
    except Exception as e:
        return f"An Error occred : {e}", 400

@app.route("/api/dataPrg/", methods=["GET"])
def dataPrg():
    '''
    Return Data on a single Date point
    '''
    try:
        bar = request.args.to_dict()
        for arg in ["prg", "sig", "date"]:
            if arg not in list(bar.keys()):
                raise Exception('Missing Querie Arguments')
            
        prgCode = bar['prg']
        signal = bar['sig']
        
        date = _get_date(bar['date'])
        #Validate Date Format 
        if date is None: 
            raise Exception("Invalid Date Format")
        
        #Normalize String Inputs
        prgCode = str(prgCode).upper()
        signal = str(signal).upper()


        if request.method == "GET":
            data, code, msg = data_controller.get_dataPrg(prgCode.upper(), signal.upper(), date)
        
        response = json.dumps( {'data': data, 'message': msg } )

        return response,code

    except Exception as e:
        return json.dumps( {'error': f'{e}'} ), 400

@app.route("/api/dataPrd/", methods=["GET"])
def dataPrd():
    '''
    Return Data based on a data range 
    '''
    try: 
        bar = request.args.to_dict()
        for arg in ["prg","sig","date1","date2"]:
            if arg not in list(bar.keys()):
                raise Exception('Missing Querie Arguments')

        prgCode = bar['prg'].upper()
        signal = bar['sig'].upper()
        date1 = _get_date(bar['date1'])
        date2 = _get_date(bar['date2'])
        
        #Validate Date Format
        if date1 is None: 
            raise Exception("Invalid Date 1 Format")
        if date2 is None:
            raise Exception("Invalid Date 2 Format")
        
        #Normalize String Inputs
        prgCode = str(prgCode).upper()
        signal = str(signal).upper()

        if request.method == "GET":
            data, code, msg = data_controller.get_dataPrd(prgCode,signal,date1,date2)
        
        response = json.dumps( {'data': data, 'message': msg} )
        

        return response, code
    
    except Exception as e:
        return json.dumps({'error':f'{e}'}), 400

def _get_date(date_string):
    format = '%d-%m-%Y'
    try:
        return datetime.strptime(date_string, format)
    except:
        return None
port = int(os.environ.get('PORT', 8080))
if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=port)
