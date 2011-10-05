__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from werkzeug.wrappers import Response
from server.utils import create_standard_json_response
from server.utils import add_standard_json_html_response_headers
from server.utils import add_503_error_html_response_headers
from server.utils import add_error_html_response_headers
from server.utils import versions
import json
import re

def error_400(request, error_message):
    response = Response('Bad Request: ' + error_message)
    response.status_code = 400
    add_error_html_response_headers(response)
    return response

def error_401(request, error_message):
    response = Response('Unauthorized: ' + error_message)
    response.status_code = 401
    add_error_html_response_headers(response)
    return response

def error_404(request, error_message):
    response = Response('Not Found: ' + error_message)
    response.status_code = 404
    add_error_html_response_headers(response)
    return response

def error_403(request, error_message):
    response = Response('Forbidden: ' + error_message)
    response.status_code = 403
    add_error_html_response_headers(response)
    return response

def error_405(request, error_message):
    response = Response('Method Not Allowed: ' + error_message)
    response.status_code = 405
    add_error_html_response_headers(response)
    return response

def error_503(request, error_message):
    response = Response('Unavailable: ' + error_message)
    response.status_code = 503
    add_503_error_html_response_headers(response)
    return response

def silcc_tag_view(api_response):
    rule = re.compile(r'^\d{3}', re.IGNORECASE)
    response_data = api_response.read()
    response_is_json = not bool(rule.match(response_data))
    if response_is_json :
        response_json = create_standard_json_response('tagger','tag','success','{"tags":%s}' % response_data)
    else :
        response_json = create_standard_json_response('tagger','tag','failure',response_data,False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "SiLCC/%s Swiftriver/%s" % (versions["silcc"], versions["swiftriver"]))
    return response

def riverid_register_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'Succeeded':
        response_json = create_standard_json_response('riverid','register','success')
    else:
        response_json = create_standard_json_response('riverid','register','failure', {'errors':data['errors']}, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "RiverID/%s Swiftriver/%s" % (versions["riverid"], versions["swiftriver"]))
    return response

def riverid_validatecredentials_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'Succeeded':
        response_json = create_standard_json_response('riverid','validatecredentials','success')
    else:
        response_json = create_standard_json_response('riverid','validatecredentials','failure', {'errors':data['errors']}, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "RiverID/%s Swiftriver/%s" % (versions["riverid"], versions["swiftriver"]))
    return response

def metalens_register_new_device_view(status, response_data):
    response_json = create_standard_json_response('metalense','submitimage',status, response_data, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "metaLayer/%s metaLens/%s" % (versions["metalayer"], versions["metalens"]))
    return response

def metalens_submit_image_view(status, response_data):
    response_json = create_standard_json_response('metalense','submitimage',status, response_data, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "metaLayer/%s metaLens/%s" % (versions["metalayer"], versions["metalens"]))
    return response

def metalens_search_for_image_view(status, response_data = None):
    response_json = create_standard_json_response('metalense','searchforimage',status, response_data, True)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "metaLayer/%s metaLens/%s" % (versions["metalayer"], versions["metalens"]))
    return response

def datalayer_full_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'failed':
        response_json = create_standard_json_response('datalayer','bundle','failure', {'errors':[data['error']]}, False)
    else:
        response_json = create_standard_json_response('datalayer','bundle','success', { 'datalayer':data['datalayer'] }, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "dataLayer/%s metaLayer/%s" % (versions["datalayer"], versions["metalayer"]))
    return response

def datalayer_sentiment_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'failed':
        response_json = create_standard_json_response('datalayer','sentiment','failure', {'errors':[data['error']]}, False)
    else:
        response_json = create_standard_json_response('datalayer','sentiment','success', { 'datalayer':{ 'sentiment':data['datalayer']['sentiment'] } }, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "dataLayer/%s metaLayer/%s" % (versions["datalayer"], versions["metalayer"]))
    return response

def datalayer_locations_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'failed':
        response_json = create_standard_json_response('datalayer','locations','failure', {'errors':[data['error']]}, False)
    else:
        response_json = create_standard_json_response('datalayer','locations','success', { 'datalayer':{ 'locations':data['datalayer']['locations'] } }, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "dataLayer/%s metaLayer/%s" % (versions["datalayer"], versions["metalayer"]))
    return response

def datalayer_tagging_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'failed':
        response_json = create_standard_json_response('datalayer','tagging','failure', {'errors':[data['error']]}, False)
    else:
        response_json = create_standard_json_response('datalayer','tagging','success', { 'datalayer':{ 'tags':data['datalayer']['tags'] } }, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "dataLayer/%s metaLayer/%s" % (versions["datalayer"], versions["metalayer"]))
    return response

def imglayer_full_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'failed':
        response_json = create_standard_json_response('imglayer','bundle','failure', {'errors':[data['error']]}, False)
    else:
        response_json = create_standard_json_response('imglayer','bundle','success', { 'datalayer':data['datalayer'], 'imglayer':data['imglayer'], 'objectdetection':data['objectdetection'] }, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "imgLayer/%s metaLayer/%s" % (versions["imglayer"], versions["metalayer"]))
    return response

def imglayer_color_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'failed':
        response_json = create_standard_json_response('imglayer','color','failure', {'errors':[data['error']]}, False)
    else:
        response_json = create_standard_json_response('imglayer','color','success', { 'imglayer':{'colors':data['imglayer']['colors']} }, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "imgLayer/%s metaLayer/%s" % (versions["imglayer"], versions["metalayer"]))
    return response

def imglayer_histogram_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'failed':
        response_json = create_standard_json_response('imglayer','histogram','failure', {'errors':[data['error']]}, False)
    else:
        response_json = create_standard_json_response('imglayer','histogram','success', { 'imglayer':{'histogram':data['imglayer']['histogram']} }, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "imgLayer/%s metaLayer/%s" % (versions["imglayer"], versions["metalayer"]))
    return response

def imglayer_ocr_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'failed':
        response_json = create_standard_json_response('imglayer','ocr','failure', {'errors':[data['error']]}, False)
    else:
        response_json = create_standard_json_response('imglayer','ocr','success', { 'datalayer': { 'text':data['datalayer']['text'], 'tags':data['datalayer']['tags'], 'locations':data['datalayer']['locations'] } }, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "imgLayer/%s metaLayer/%s" % (versions["imglayer"], versions["metalayer"]))
    return response

def imglayer_facedetection_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'failed':
        response_json = create_standard_json_response('imglayer','facedetection','failure', {'errors':[data['error']]}, False)
    else:
        response_json = create_standard_json_response('imglayer','facedetection','success', { 'objectdetection':data['objectdetection'] }, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "imgLayer/%s metaLayer/%s" % (versions["imglayer"], versions["metalayer"]))
    return response

def snipsnap_tagging_view(api_response):
    json_string = api_response.read()
    data = json.loads(json_string)
    if data['status'] == 'failed':
        response_json = create_standard_json_response('snipsnap','tagging','failure', {'errors':[data['error']]}, False)
    else:
        response_json = create_standard_json_response('snipsnap','tagging','success', { 'datalayer':{ 'tags':data['datalayer']['tags'] } }, False)
    response = Response(response_json)
    add_standard_json_html_response_headers(response)
    response.headers.add("Server", "dataLayer/%s metaLayer/%s" % (versions["datalayer"], versions["metalayer"]))
    return response

