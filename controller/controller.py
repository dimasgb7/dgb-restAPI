import json
import pandas
from datetime import datetime
from services import loader

ldr = loader.loader_interface()

def get_dataPrg(prgCod, signal, date):
    
    _sample = ldr.get_sample(prgCod, signal, date)
    if _sample:
        sp = _sample[0].to_dict()
        data = {'available_time': sp['available_time'],'predicted_audience':sp['predicted_audience']} 
        code = 200
        message = 'Success'
    else:
        data = {} 
        code = 404
        message = 'No data available'
     
    return data, code, message

def get_dataPrd(prgCod, signal, date1, date2):
    _samples = ldr.get_sample_onRange(prgCod, signal, date1, date2)
    if _samples:
        samples = [ _sp.to_dict() for _sp in _samples]
        
        res = [{
                'date':datetime.strftime(sp['date'], '%d-%m-%Y'), 
                'available_time': sp['available_time'], 
                'predicted_audience': sp['predicted_audience']
                } for sp in samples ]
            
        code = 200
        message = 'Success'
    else:
        res = {}
        code = 404
        message = 'No data available'
    
    return res, code, message
