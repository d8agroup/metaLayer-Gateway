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

def spling_image_search(request, api_method_wrapper):
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

    tags_for_image_search = tags['datalayer']['tags']

    tags_for_image_search = sorted(tags_for_image_search, key=lambda x: len(x), reverse=True)

    tags_for_image_search = tags_for_image_search[0:4]

    image_search_url = 'http://api.bing.net/json.aspx?Appid=53FD9766868189E3BEDC3527303DA39249975A19&query=%s&sources=image' % '%20'.join(tags_for_image_search)

    response = urllib2.urlopen(image_search_url).read()

    response = json.loads(response)

    images = response['SearchResponse']['Image']['Results']

    return_images = []

    for image in images:
        return_images.append({
            'width':image['Width'],
            'height':image['Height'],
            'title':image['Title'],
            'url':image['MediaUrl']
        })

    new_response = StringIO.StringIO(json.dumps({'imglayer':{'images':return_images}}))

    return view(new_response)

