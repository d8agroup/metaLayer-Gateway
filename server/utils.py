__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from werkzeug.local import Local, LocalManager
from configuration.configuration import config
from oauth2 import Request
from threading import Thread
import json
import urllib2
import re
import logging
import logging.handlers


#Basic wgis setup
local = Local()
local_manager = LocalManager([local])
application = local('application')

#version number
versions = {
    "python":"2.7.1",
    "werkzeug":"0.6.2",
    "swiftriver":"0.5.6",
    "swiftgateway":"0.1",
    "silcc":"0.1",
    "riverid":"0.1",
    "metalayer":"0.1",
    "metalens":"0.0.1",
    "datalayer":"0.0.1",
    "imglayer":"0.0.1"
}

#server logging
baselogging_filename = config.get('baselogging', 'filename')
baselogger = logging.getLogger('baselogger')
formatter = logging.Formatter('%(created)f, %(name)s, %(levelname)s, %(module)s, %(funcName)s, %(lineno)s, %(message)s')
logging_handler = logging.handlers.TimedRotatingFileHandler(baselogging_filename, when='d', interval=1, backupCount=30, encoding=None, delay=False, utc=False)
logging_handler.setFormatter(formatter)
baselogger.addHandler(logging_handler)

def async(gen):
    def func(*args, **kwargs):
        it = gen(*args, **kwargs)
        result = it.next()
        Thread(target=lambda: list(it)).start()
        return result
    return func

class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result

def map_path_to_api_wrapper_identifier(path):
    if path == None or len(path) < 1 or unicode(path) == u'/':
        return None
    identifier_parts = path.lstrip('/').split('/')
    if len(identifier_parts) < 2:
        return None
    identifier = "%s/%s" % (identifier_parts[0], identifier_parts[1])
    return unicode(identifier)

def create_standard_json_response(api_identifier, api_method, status, response=None, response_is_json=True):
    if response == None:
        json_response = json.dumps({'service': api_identifier,'method': api_method,'status': status})
    elif response_is_json :
        response_as_dict = json.loads(response)
        json_response = json.dumps({'service': api_identifier,'method': api_method,'status': status,'response':response_as_dict})
    else :
        json_response = json.dumps({'service': api_identifier,'method': api_method,'status': status,'response':response})
    return unicode(json_response, "utf-8")

def add_error_html_response_headers(response):
    response.headers.add('Server', 'SwiftGateway/%s Werkzeug/%s Python/%s' % (versions['swiftgateway'], versions['werkzeug'], versions['python']))

def add_503_error_html_response_headers(response):
    add_error_html_response_headers(response)
    response.headers.add("Retry-After", "60")

def add_standard_html_response_headers(response):
    response.headers.add('Via', 'SwiftGateway/%s Werkzeug/%s Python/%s' % (versions['swiftgateway'], versions['werkzeug'], versions['python']))

def add_standard_json_html_response_headers(response):
    add_standard_html_response_headers(response)
    response.content_type = 'application/json; charset=utf-8'
    
def is_oauth_request(request):
    oauth_request = False
    if 'Authorization' in request.headers :
        oauth_rule = re.compile(r'^oauth', re.IGNORECASE)
        authorization = request.headers['Authorization'].strip()
        oauth_request = bool(oauth_rule.match(authorization))
    if 'oauth_consumer_key' in request.args.keys():
        oauth_request = True
    return oauth_request


def extract_oauth_consumer_key_from_auth_header_string(auth_header_string):
    if not auth_header_string:
        return None
    items = urllib2.parse_http_list(auth_header_string)
    opts = urllib2.parse_keqv_list(items)
    if not 'oauth_consumer_key' in opts:
        return None
    return opts['oauth_consumer_key']

def build_oauth_request_from_request(method, url, auth_header):
    return Request.from_request(method, url, auth_header)

def safe_save_usage_statistics_stage_two(usage_statistics, failed=False):
    try:
        usage_statistics.save_stage_two()
    except Exception, e:
        baselogger.error("USAGE STATISTICS RECORDING ERROR , |%s|" % e)
        baselogger.error("USAGE STATISTICS REPLAY, |%s|" % usage_statistics.sql_dump())

def safe_save_usage_statistics_stage_one(usage_statistics):
    try:
        usage_statistics.save_stage_one()
    except Exception, e:
        baselogger.error("USAGE STATISTICS RECORDING ERROR , |%s|" % e)
        baselogger.error("USAGE STATISTICS REPLAY, |%s|" % usage_statistics.sql_dump())