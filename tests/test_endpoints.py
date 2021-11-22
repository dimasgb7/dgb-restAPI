import pytest
import requests

url = 'http://127.0.0.1:5000'
dataPrg_url = url+'/api/dataPrg/'
dataPrd_url = url+'/api/dataPrd/'

def test_index_page():
    r = requests.get(url+'/')
    assert r.status_code == 200 

def test_dataPrg_UNIT():
    _querie = _prgQuerie('VALE','SP1','22-07-2020')
    _request = dataPrg_url + _querie
    r = requests.get(_request)
    
    data = r.json()
    assert data['data']['available_time'] == 224
    assert data['message'] == 'Success'
    assert r.status_code == 200

def test_dataPrd_UNIT():
    _querie = _prdQuerie('VALE','SP1','22-07-2020','28-07-2020')
    _request = dataPrd_url + _querie
    r = requests.get(_request)

    resp = r.json()
    data_pack = resp['data']
    
    assert len(data_pack) == 5
    assert resp['message'] == 'Success'
    assert r.status_code == 200

def test_dataPrg():
    prg_l = ['VALE','HUCK']
    sig_l = ['SP1','SP1']
    date_l = ['22-07-2020','25-07-2020']
    
    for prg, sig, date in zip(prg_l,sig_l, date_l):
        _querie = _prgQuerie(prg,sig,date)
        _request = dataPrg_url + _querie
        r = requests.get(_request)
        assert r.status_code == 200

def test_NO_DATA_FOUND():
    _querie = _prgQuerie('VALE','SP1','22-07-2045')
    _request = dataPrg_url + _querie
    r = requests.get(_request)
    
    data = r.json()
    assert data['data'] == {}

    assert data['message'] == 'No data available'
    assert r.status_code == 404

def test_INVALID_DATE_FORMAT():
    _querie = _prgQuerie('VALE','SP1','22/07/2020')
    _request = dataPrg_url + _querie
    r = requests.get(_request)
    
    data = r.json()
    assert data['error']
    assert r.status_code == 400

def test_VERY_LARGE_RANGE():
    _querie  = _prdQuerie('HUCK', 'SP1', '01-01-1820','12-12-2142')
    _request = dataPrd_url + _querie
    r = requests.get(_request)

    resp = r.json()
    data_pack = resp['data']
    assert len(data_pack) > 0
    assert resp['message'] == 'Success'
    assert r.status_code == 200

def test_NO_RANGE():
    _querie  = _prdQuerie('HUCK', 'SP1', '01-08-2020','01-08-2020')
    _request = dataPrd_url + _querie
    r = requests.get(_request)

    resp = r.json()
    data_pack = resp['data']
    assert len(data_pack) == 1
    assert resp['message'] == 'Success'
    assert r.status_code == 200


def _prgQuerie(PRG_CODE,SIG,DATE):
    return '?prg='+PRG_CODE+'&sig='+SIG+'&date='+DATE

def _prdQuerie(PRG_CODE,SIG,DATE1,DATE2):
    return '?prg='+PRG_CODE+'&sig='+SIG+'&date1='+DATE1+'&date2='+DATE2
