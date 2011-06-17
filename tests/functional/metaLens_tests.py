__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"

import oauth2
import time
import urllib2
import urllib
import hashlib
from urllib2 import URLError


def build_request(key, secret, url, method='POST', values={}):
    params = {
        'oauth_timestamp': int(time.time()),
        'oauth_nonce': None,
        'oauth_signature_method':'HMAC-SHA1',
    }
    params.update(values)
    consumer = oauth2.Consumer(key=key,secret=secret)
    req = oauth2.Request(method=method, url=url, parameters=params)
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, None)
    return req

def test_registernewdevice():
    #development
    key = 'e1ec82eb8c75be208b31a138250550bf8142a418a8c76c48aa608664'
    secret = '490476246e90d47179859114bb9c66cc43c25a86b84573c4b91763a8'
    url = 'http://local.mlgateway.com/metalens/1/registernewdevice'    
    values = {
        'deviceguid':hashlib.sha224("%s" % time.time()).hexdigest()
    }
    request = build_request(key, secret, url, values=values)
    data = urllib.urlencode(values)
    try :
        req = urllib2.Request(url, headers=request.to_header(), data=data)
        u = urllib2.urlopen(req)
        print u.read()
    except URLError, e:
        print e

def test_submitimage():
    #development
    key = '99eb8dd8b781a170b7c2168e281f5a66e2ac31459cee99b7ae371943'
    secret = 'e0699de40979b6b2a15552659b08ca4c00f70c13800b7c657ee7c9f3'
    url = 'http://local.mlgateway.com/metalens/1/submitimage'    
    values = {
        
    }
    request = build_request(key, secret, url, values=values)
    data = urllib.urlencode(values)
    try :
        req = urllib2.Request(url, headers=request.to_header(), data=data)
        u = urllib2.urlopen(req)
        print u.read()
    except URLError, e:
        print e


#test_registernewdevice()
test_submitimage()