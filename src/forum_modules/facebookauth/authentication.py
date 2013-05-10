import cgi
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
    _parse_json = lambda s: simplejson.loads(s, 'utf-8')
except ImportError:
    # For Google AppEngine
    from django.utils import simplejson
    _parse_json = lambda s: simplejson.loads(s)

REST_SERVER = 'http://api.facebook.com/restserver.php'
GRAPH_API_USER = 'https://graph.facebook.com/me?'
GRAPH_API_ACCESS_TOKEN = 'https://graph.facebook.com/oauth/access_token?'

class FacebookAuthConsumer(AuthenticationConsumer):
    
    def process_authentication_request(self, request):
        response = self.parse_fb_cookie(request.COOKIES)
        return response['user_id']
        
    def urlsafe_b64decode(self, str):
        l = len(str)
        pl = l % 4
        return base64.urlsafe_b64decode(str.ljust(l+pl, "="))
 
 
    def parse_signed_request(self, signed_request, secret):
        if "." in signed_request:
            esig, payload = signed_request.split(".")
        else:
            return {}

        sig = self.urlsafe_b64decode(str(esig))
        data = _parse_json(self.urlsafe_b64decode(str(payload)))

        if not isinstance(data, dict):
            raise InvalidAuthentication(_("Pyload is not a json string!"))
            return {}

        if data["algorithm"].upper() == "HMAC-SHA256":
            if hmac.new(secret, payload, hashlib.sha256).digest() == sig:
                return data

        else:
            raise InvalidAuthentication(_("Not HMAC-SHA256 encrypted!"))

        return {}
        
    def parse_fb_cookie(self, cookies):
        API_KEY = str(settings.FB_API_KEY)
        cookieName = 'fbsr_'+API_KEY

        if cookieName in cookies:
            cookieData = cookies['fbsr_'+API_KEY]
            app_secret = str(settings.FB_APP_SECRET)
            response = self.parse_signed_request(cookieData, app_secret)
            if response:
                return response
        
        raise InvalidAuthentication(_('The authentication with Facebook connect failed, cannot find authentication tokens'))
        
    def get_user_data(self, key, cookies):
        request_data = {
            'fields': 'username,email'
        }

        parsed_data = self.parse_fb_cookie(cookies)
        
        if parsed_data['user_id'] != key:
             raise InvalidAuthentication(_('Invalid cookie, please clear your cookies then try again'))
        
        args = dict(
            code = parsed_data['code'],
            client_id = str(settings.FB_API_KEY),
            client_secret = str(settings.FB_APP_SECRET),
            redirect_uri = '',
        )
     
        file = urlopen(GRAPH_API_ACCESS_TOKEN + urlencode(args))
        try:
            token_response = file.read()
        finally:
            file.close()
     
        access_token = cgi.parse_qs(token_response)["access_token"][-1]
        
        request_data['access_token'] = access_token
        query_resp = urlopen(GRAPH_API_USER + urlencode(request_data)).read()
        fb_response = _parse_json(query_resp)

        user_email = ""
        if 'email' in fb_response:
            user_email = fb_response['email']
        
        return {
            'username': fb_response['username'],
            'email': user_email
        }


class FacebookAuthContext(ConsumerTemplateContext):
    mode = 'BIGICON'
    type = 'CUSTOM'
    weight = 100
    human_name = 'Facebook'
    code_template = 'modules/facebookauth/button.html'
    extra_css = ["http://www.facebook.com/css/connect/connect_button.css"]

    API_KEY = settings.FB_API_KEY
