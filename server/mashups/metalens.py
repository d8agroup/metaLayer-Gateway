from server import views
from server import mappers
from urllib2 import urlopen, HTTPError, Request
from urllib import urlencode
from domain.utils import get_authenticated_user_by_riverid
from domain.utils import get_all_price_plans_for_app_template, create_new_subscription, con
from lib.pytesser.pytesser import *
from configuration.configuration import config
import re
import time
import hashlib
import json
import os
from domain.models import *
from server.utils import baselogger
from server.utils import async

def run_register_new_device_adapter(request, api_method_wrapper):
    view = getattr(views, api_method_wrapper.view)
    
    device_guid = request.form.get('deviceguid')
    
    if not device_guid:
        return view('failure', {"errors":["You did not include a guid for this device"]})
    
    metalens_account = get_authenticated_user_by_riverid("metalens")
    
    candidate_apps = [app for app in metalens_account.apps if app.key == device_guid]
    
    if candidate_apps:
        user_app = candidate_apps[0]
    else:
        metalens_price_plans = get_all_price_plans_for_app_template('metalens/1', "admin")
        
        #TODO Here we need to add support for creating paid accounts too
        price_plan = [p for p in metalens_price_plans if p.name == "A metaLens Device"][0]
        
        subscription_id = create_new_subscription(int(time.time()), 0, price_plan)
        
        user_app_name = 'A metaLens Device %s' % device_guid
        user_app_key = device_guid
        user_app_secret_seed = "%s %s %s" % (unicode(metalens_account._id), user_app_name, time.time())
        user_app_secret = hashlib.sha224(user_app_secret_seed).hexdigest()
        user_app_template = unicode(con.AppTemplate.find_one({'name':'A metaLens Device'})._id)
        user_app = AuthenticatedUserApp({
            "name":user_app_name,
            "key":user_app_key,
            "secret":user_app_secret,
            "subscription_ids":[subscription_id],
            "template":user_app_template})
        metalens_account.apps.append(user_app)
        metalens_account.save()
        
    return view('success', {'key':user_app.key, 'secret':user_app.secret})

@async
def run_submit_image_adapter(request, api_method_wrapper):
    view = getattr(views, api_method_wrapper.view);
    
    file = request.files.get('image')
    
    filename = int(time.time())
    
    file.save("/tmp/%s.tif" % filename)
    
    image = Image.open("/tmp/%s.tif" % filename)
    
    text = image_to_string(image)
    
    text = re.sub('\\n', ' ', text)
    
    image = None
    
    os.unlink("/tmp/%s.tif" % filename)

    is_text = len(text.strip(' \t\n\r')) != 0
    
    if(is_text):
        return_data = view('success', {"message":"Text was extracted from your image and has been submitted for processing"})
    else:
        return_data = view('failure', {"message":"No text could be extracted from the image"})    
    
    yield return_data
    
    core_api_request = "%sapi/channelservices/pushtochannel.php" % config.get('services', 'core')
    
    core_api_parameters = {
        "deviceid":request.form.get('deviceid'),
        "imageid":request.form.get('imageid'),
        "key":request.form.get('deviceid'),
        "origin":"MetalensImageText",
        "text":text
    }
    
    request = Request(url=core_api_request, data=urlencode(core_api_parameters))
    
    try:
        urlopen(request)
    except HTTPError, e:
        baselogger.error("%s" % e)


def run_search_for_image_adapter(request, api_method_wrapper):
    view = getattr(views, api_method_wrapper.view);
    
    core_api_request = "%sapi/contentservices/getcontent.php" % config.get('services', 'core')
    
    core_api_parameters = {
        "json":'{"id":"%s"}' % request.form.get('imageid'),
        "key":request.form.get('deviceid'),
    }
    
    request = Request(url=core_api_request, data=urlencode(core_api_parameters))
    
    try:
        response = urlopen(request)
        
        response_data = response.read()
        
        return view('success', response_data)
    
    except HTTPError, e:
        baselogger.error("%s" % e)
        
        return view('failure')