import urllib2, urllib
import server.views as views  
import StringIO
import json

def snipsnap_full(request, api_method_wrapper):
    view = getattr(views, api_method_wrapper.view)
    
    if 'text' not in request.form:
        return view(StringIO.StringIO('{"status":"failed", "error":"You did not include the required POST field text"}'))
        
    text = unicode(request.form.get('text')).encode('utf-8')
    
    url = api_method_wrapper.endpoint
    
    data = { 'text':text }
    
    data = urllib.urlencode(data)
    
    request = urllib2.Request(url, data=data)
    
    response = urllib2.urlopen(request)
    
    tags = json.loads(response.read())
    
    black_list = ['coupon', 'limit', 'offer', 'expire', 'cannot', 'combined', 'any', 'coupon', 'presented', 'anytime', 'not', 'valid', 'on', 'prior', 'purchase']
    
    new_tags = []
    
    for tag in tags['datalayer']['tags']:
        if tag.lower() not in black_list:
            new_tags.append(tag)
    
    tags['datalayer']['tags'] = new_tags
    
    new_response = StringIO.StringIO(json.dumps(tags))
    
    return view(new_response)

    