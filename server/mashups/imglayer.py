from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
import server.views as views
import urllib2, urllib


def imglayer_full(request, api_method_wrapper):
    view = getattr(views, api_method_wrapper.view)
    
    image = request.files.get('image')
    
    if not image:
        view('failure', {"errors":["You did not include the required POST file \"image\""]})
        
    url = api_method_wrapper.endpoint
    
    register_openers()

    items = []
    
    items.append(MultipartParam(name='image', filename='image.tiff', fileobj=image))

    datagen, headers = multipart_encode(items)

    request = urllib2.Request(url, datagen, headers)

    response = urllib2.urlopen(request)

    return view(response)
