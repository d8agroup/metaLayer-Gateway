from server.mashups.spling import spling_full, spling_image_search

__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from werkzeug.wrappers import Response
from server import views
from server import mappers
from urllib2 import urlopen, HTTPError
from server.mashups.metalens import run_submit_image_adapter
from server.mashups.metalens import run_register_new_device_adapter  
from server.mashups.metalens import run_search_for_image_adapter
from server.mashups.datalayer import datalayer_full
from server.mashups.imglayer import imglayer_full
from server.mashups.snipsnap import snipsnap_full
from server.mashups.kwelia import kwelia_full
from server.mashups.tedglobe import tedglobe_full

def generic_error_handler(request, error_code, error_message):
    #TODO: Pass the error_message to the view
    error_view_name = "error_" + error_code
    error_view = getattr(views, error_view_name)
    return error_view(request, error_message)

def generic_api_request_handler(request, api_method_wrapper):
    """Maps and formats the incoming request and calls the underlying API service"""
    #get the mapper function for this path
    mapper = getattr(mappers, api_method_wrapper.mapper)

    #map the original request onto the api_request
    api_request = mapper(request, api_method_wrapper.endpoint)

    try:
        #call the underying api
        response = urlopen(api_request)

        #extract which view should be used to process the api response
        view = getattr(views, api_method_wrapper.view)

        #use the view to render the response
        return view(response)

    except HTTPError, e:
        #TODO: This needs to be converted into a SwiftGateway error
        pass
    
def datalayer_handler(request, api_method_wrapper):
    return datalayer_full(request, api_method_wrapper)

def imglayer_handler(request, api_method_wrapper):
    return imglayer_full(request, api_method_wrapper)

def snipsnap_handler(request, api_method_wrapper):
    return snipsnap_full(request, api_method_wrapper)

def spling_handler(request, api_method_wrapper):
    if api_method_wrapper.method_identifier == 'image_search':
        return spling_image_search(request, api_method_wrapper)
    return spling_full(request, api_method_wrapper)


def kwelia_handler(request, api_method_wrapper):
    return kwelia_full(request, api_method_wrapper)

def metalens_handler(request, api_method_wrapper):
    if api_method_wrapper.method_identifier == 'registernewdevice':
        return run_register_new_device_adapter(request, api_method_wrapper)
    elif api_method_wrapper.method_identifier == 'submitimage':
        return run_submit_image_adapter(request, api_method_wrapper)
    elif api_method_wrapper.method_identifier == 'searchforimage':
        return run_search_for_image_adapter(request, api_method_wrapper)
    view = getattr(views, 'error_404')
    return view(request, 'The method you were looking for is not supported')

def tedglobe_handler(request, api_method_wrapper):
    if api_method_wrapper.method_identifier == 'locations':
        return datalayer_full(request, api_method_wrapper)
    return tedglobe_full(request, api_method_wrapper)