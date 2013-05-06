import base64
import hashlib
import hmac
from time import time
from datetime import datetime
from urllib import urlopen,  urlencode
from forum.authentication.base import AuthenticationConsumer, ConsumerTemplateContext, InvalidAuthentication
from django.utils.translation import ugettext as _

import settings
try:
    import simplejson
    _parse_json = lambda s: simplejson.loads(s)
except ImportError:
    # For Google AppEngine
    from django.utils import simplejson
    _parse_json = lambda s: simplejson.loads(s)

REST_SERVER = 'http://api.facebook.com/restserver.php'

class FacebookAuthConsumer(AuthenticationConsumer):
    
    def process_authentication_request(self, request):
        API_KEY = str(settings.FB_API_KEY)
        cookieName = 'fbsr_'+API_KEY

        if cookieName in request.COOKIES:
            cookieData = request.COOKIES['fbsr_'+API_KEY]
            app_secret = str(settings.FB_APP_SECRET)
            response = parse_signed_request(cookieData, app_secret)
                
            return response['user_id'] 
        else:
            raise InvalidAuthentication(_('The authentication with Facebook connect failed, cannot find authentication tokens'))

    def generate_signature(self, values):
        keys = []

        for key in sorted(values.keys()):
            keys.append(key)

        signature = ''.join(['%s=%s' % (key,  values[key]) for key in keys]) + str(settings.FB_APP_SECRET)
        return hashlib.md5(signature).hexdigest()

    def check_session_expiry(self, request, cookieName):
        import Cookie
    
        c = Cookie.SmartCookie()
        c.load(request.META['HTTP_COOKIE'])
        cookieExpiry = c[cookieName]['max-age']
        return datetime.fromtimestamp(cookieExpiry) > datetime.now()

    def check_cookies_signature(self, cookies):
        API_KEY = str(settings.FB_API_KEY)

        cookieName = 'fbsr_'+API_KEY
        
        app_secret = str(settings.FB_APP_SECRET)

        return self.generate_signature(values) == cookies[API_KEY]

    def get_user_data(self, key):
        request_data = {
            'method': 'Users.getInfo',
            'api_key': settings.FB_API_KEY,
            'call_id': time(),
            'v': '1.0',
            'uids': key,
            'fields': 'name,first_name,last_name,email',
            'format': 'json',
        }

        request_data['sig'] = self.generate_signature(request_data)
        query_resp = urlopen(REST_SERVER, urlencode(request_data)).read()
        fb_response = _parse_json(query_resp)[0]

        return {
            'username': fb_response['first_name'] + ' ' + fb_response['last_name'],
            'email': fb_response['email']
        }

def urlsafe_b64decode(str):
        l = len(str)
        pl = l % 4
        return base64.urlsafe_b64decode(str.ljust(l+pl, "="))
 
 
def parse_signed_request(signed_request, secret):
    if "." in signed_request:
        esig, payload = signed_request.split(".")
    else:
        return {}

    sig = urlsafe_b64decode(str(esig))
    data = _parse_json(urlsafe_b64decode(str(payload)))

    if not isinstance(data, dict):
        raise InvalidAuthentication(_("Pyload is not a json string!"))
        return {}

    if data["algorithm"].upper() == "HMAC-SHA256":
        if hmac.new(secret, payload, hashlib.sha256).digest() == sig:
            return data

    else:
        raise InvalidAuthentication(_("Not HMAC-SHA256 encrypted!"))

    return {}

class FacebookAuthContext(ConsumerTemplateContext):
    mode = 'BIGICON'
    type = 'CUSTOM'
    weight = 100
    human_name = 'Facebook'
    code_template = 'modules/facebookauth/button.html'
    extra_css = ["http://www.facebook.com/css/connect/connect_button.css"]

    API_KEY = settings.FB_API_KEY
