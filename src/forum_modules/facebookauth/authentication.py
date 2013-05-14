import cgi
import base64
import hashlib
import hmac
from time import time
from datetime import datetime
from urllib import urlopen,  urlencode
from forum.authentication.base import AuthenticationConsumer, ConsumerTemplateContext, InvalidAuthentication
from forum import settings as django_settings
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

import settings
try:
    import simplejson
    _parse_json = lambda s: simplejson.loads(s, 'utf-8')
except ImportError:
    # For Google AppEngine
    from django.utils import simplejson
    _parse_json = lambda s: simplejson.loads(s)

DIALOG_API = 'https://www.facebook.com/dialog/oauth/?'
GRAPH_API_USER = 'https://graph.facebook.com/me?'
GRAPH_API_ACCESS_TOKEN = 'https://graph.facebook.com/oauth/access_token?'

class FacebookAuthConsumer(AuthenticationConsumer):
    
    def prepare_authentication_request(self, request, redirect_to):
        params = dict(
                client_id = str(settings.FB_API_KEY),
                redirect_uri = "%s%s" % (django_settings.APP_URL, redirect_to),
                scope = 'email'
        )
                
        facebook_authenticate_url = DIALOG_API + urlencode(params)
        return facebook_authenticate_url
    
    def process_authentication_request(self, request):
        params = dict(
                client_id = str(settings.FB_API_KEY), 
                client_secret = str(settings.FB_APP_SECRET),
                redirect_uri="%s%s" % (django_settings.APP_URL, request.path)
        )

        if 'code' in request.GET:
            params["code"] = request.GET.get("code", '')
        else:
            raise InvalidAuthentication(_("Something wrong happened, the authentication with Facebook connect failed"))
        
        try:
            response = cgi.parse_qs(urlopen(GRAPH_API_ACCESS_TOKEN + urlencode(params)).read())
            access_token = response["access_token"][-1]

            user_data = self.get_user_data(key=access_token, req_fields='id')
            assoc_key = user_data["id"]

            request.session["access_token"] = access_token
            request.session["assoc_key"] = assoc_key

            return assoc_key
        except Exception, e:
            raise InvalidAuthentication(_("Something wrong happened, the authentication with Facebook connect failed"))
        
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
                
    def get_user_data(self, key, req_fields='username,email,id'):
        
        request_data = {
            'access_token' : key,
            'fields': req_fields
        }
        
        query_resp = urlopen(GRAPH_API_USER + urlencode(request_data)).read()
        fb_response = _parse_json(query_resp)

        if 'email' in fb_response:
            fb_response['email'] = smart_unicode(fb_response['email'])
            # If user email is longer than 75 characters (Django limit for email field) - leave it blank
            if len(fb_response['email']) > 75:
                fb_response['email'] = ''
        
        if 'username' in fb_response:
            # If the name is longer than 30 characters - leave it blank
            if len(fb_response['username']) > 30:
                fb_response['username'] = ''
        
        return fb_response


class FacebookAuthContext(ConsumerTemplateContext):
    mode = 'BIGICON'
    type = 'DIRECT'
    weight = 100
    human_name = 'Facebook'
    icon = '/media/images/openid/facebook.gif'

    API_KEY = settings.FB_API_KEY
