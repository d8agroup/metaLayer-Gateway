from server import views
from server import mappers
from urllib2 import urlopen, HTTPError
from domain.utils import get_authenticated_user_by_riverid
from domain.utils import get_all_price_plans_for_app_template, create_new_subscription, con
import re
import time
import hashlib
import json
from domain.models import *

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

def run_submit_image_adapter(request, api_method_wrapper):
    view = getattr(views, api_method_wrapper.view);
    
    return view('success', {"nothing":"something"})