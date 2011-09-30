import urllib2, urllib
import server.views as views  
import StringIO

def datalayer_full(request, api_method_wrapper):
    view = getattr(views, api_method_wrapper.view)
    
    text = request.form.get('text')
    
    if not text:
        view(StringIO.StringIO('{"status":"failed", "errors":["You did not include the required POST field text"]}'))
        
    url = api_method_wrapper.endpoint
    
    data = { 'text':text }
    
    data = urllib.urlencode(data)
    
    request = urllib2.Request(url, data=data)
    
    response = urllib2.urlopen(request)
    
    return view(response)

    