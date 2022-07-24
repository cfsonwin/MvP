import re

from django.shortcuts import redirect
from django.urls import reverse


class UserLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('UserLoginMiddleware')
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # if already login
        if re.match(r'^/uid', request.path):
            print(request.path)
            u_id = request.path.split('/')[1].split('?')[-1]
            if request.session.get('already_login_user') == None or (int(u_id) not in request.session.get('already_login_user')['u_id']):
                print("%s not in list: " % u_id, request.session.get('already_login_user')['u_id'])
                return redirect(reverse('mU_signin'))
            if 'already_login_user' not in request.session:
                return redirect(reverse('mU_signin'))
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
