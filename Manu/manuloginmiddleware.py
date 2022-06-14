import re
from django.shortcuts import redirect
from django.urls import reverse

class ManuLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('ManuLoginMiddleware')
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('**********url: ', request.path)

        # if already login
        urllist = ['/manu/signin/', '/manu/dosignin/', '/manu/signout/', '/manu/signup/', '/manu/signupcheck/']
        if re.match(r'^/manu', request.path) and (request.path not in urllist):
            if ('already_login_manu' not in request.session) or (request.path == '/manu'):
                return redirect(reverse('mM_signin'))
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
