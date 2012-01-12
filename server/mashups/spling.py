import urllib2, urllib
import server.views as views
import StringIO
import json

def spling_full(request, api_method_wrapper):
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

    new_response = StringIO.StringIO(json.dumps(tags))

    return view(new_response)

    