from django.template import RequestContext, loader
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
import os
from arsoft.kerberos.kpasswd import kpasswd
from arsoft.kerberos.kinit import kinit
from urllib.parse import urlencode, quote_plus


def redirect_params(url, params=None):
    response = redirect(url)
    if params:
        query_string = urlencode(params, quote_via=quote_plus)
        response['Location'] += '?' + query_string
    return response

def _get_request_data(request, *args, **kwargs):

    realm = None
    password = None
    oldpassword = None
    newpassword = None

    username = kwargs.get('username')
    try:
        username = request.session.get('username')
        result = request.session.get('result')
        if result:
            status_message = request.session['error_message']
            error_message = ''
        else:
            error_message = request.session['error_message']
            status_message = ''
    except (KeyError):
        error_message = ''
        status_message = ''
        username = ''
        pass

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
    elif request.method == 'GET':
        username = request.GET.get('username')

    if not username and 'REMOTE_USER' in request.META:
        username = request.META['REMOTE_USER']
    if not username and 'HTTP_REMOTE_USER' in request.META:
        username = request.META['HTTP_REMOTE_USER']
    if not username and 'HTTP_AUTHORIZATION' in request.META:
        username = request.META['HTTP_AUTHORIZATION']

    # drop of the REALM part if there's any
    if username and '@' in username:
        (username, realm) = username.split('@', 1)

    if not realm and 'HTTP_REALM' in request.META:
        realm = request.META['HTTP_REALM']
    if not realm:
        realm = os.getenv('REALM', None)

    return {'username': username, 'realm': realm, 
            'password': password,
            'newpassword': newpassword,
            'oldpassword': oldpassword,
            'errormessage': error_message, 'statusmessage': status_message}

def login(request, *args, **kwargs):

    title = 'Change password service'
    data = _get_request_data(request)

    if request.method == 'POST':
        (ret, error_message) = kinit(data['username'], data['password'])
        if ret:
            return redirect_params(reverse(home), params={'username': data['username']})
        else:
            # remove the password to avoid password capture
            data['password'] = ''
            data['errormessage'] = error_message
    if data['password'] is None:
        data['password'] = ''

    t = loader.get_template('login.html')
    print(data)
    return HttpResponse(t.render(data, request))


def home(request, *args, **kwargs):
    data = _get_request_data(request)

    if not data['username']:
        return redirect_params(reverse(login))
    else:
        title = 'Change password service'

        t = loader.get_template('home.html')
        data['title'] = title
        return HttpResponse(t.render(data, request))

def changepw(request, *args, **kwargs):
    data = _get_request_data(request, args=args, kwargs=kwargs)

    if request.method == 'POST':
        if data['username']:
            if data['newpassword'] != data['confpassword']:
                error_message = 'New password and confirmation password do not match.'
                result_code = False
            elif data['oldpassword'] == '':
                error_message = 'Current password not specified.'
                result_code = False
            elif data['newpassword'] == '':
                error_message = 'No new password specified.'
                result_code = False
            else:
                (ret, error_message) = kpasswd(data['username'], data['oldpassword'], data['newpassword'])
                if ret:
                    error_message = 'Successful.'
                    result_code = True
                else:
                    error_message = 'Failed to change password. ' + error_message
                    result_code = False
        else:
            error_message = 'No user name specified.'
            result_code = False

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        request.session['username'] = data['username']
        request.session['error_message'] = error_message
        request.session['result'] = result_code
        return redirect_params(reverse(home), params={'username': data['username']})
    else:
        return redirect_params(reverse(home))
