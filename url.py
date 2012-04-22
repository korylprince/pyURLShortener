#!/usr/bin/python

"""
Simple url shortener.
Requests to host/i/http://site/
returns a code.
requests to host/o/code
redirects to http://site/
"""
import memcache
import string
import random


def application(env, start_response):
    """
    main application
    """
    # get input
    request = env['REQUEST_URI']
    mc = memcache.Client(['127.0.0.1:11211'])
    # if putting with subfolder
    if '/i/' in request:
        # generate code
        char_set = string.letters+string.digits
        code = ''.join(random.sample(char_set,4))
        # make sure imput happened
        if not mc.set(code,request[3:]):
            start_response('200 OK', [('Content-Type','text/plain')])
            return 'error'
        # send back code
        start_response('200 OK', [('Content-Type','text/plain')])
        return getURLBase(env)+'/o/'+code

    # if putting no subfolder
    elif '/in/' in request:
        # generate code
        char_set = string.letters+string.digits
        code = ''.join(random.sample(char_set,4))
        # make sure imput happened
        if not mc.set(code,request[4:]):
            start_response('200 OK', [('Content-Type','text/plain')])
            return 'error'
        # send back code
        start_response('200 OK', [('Content-Type','text/plain')])
        return getURLBase(env)+'/'+code
    
    # if getting subfolder
    elif '/o/' in request:
        code = mc.get(request[3:])
        # no code
        if code == None:
            start_response('200 OK', [('Content-Type','text/html')])
            return '<h1>URL Not Found</h1>'
        # we do have a code for it
        start_response('301 Moved Permanently', [('Location',code)])
        return 0

    # if getting no subfolder
    else:
        code = mc.get(request[1:])
        # no code
        if code == None:
            start_response('200 OK', [('Content-Type','text/html')])
            return '<h1>URL Not Found</h1>'
        # we do have a code for it
        start_response('301 Moved Permanently', [('Location',code)])
        return 0

def getURLBase(env):
    """
    returns http(s)://server(:port) part of url
    """
    if (env['UWSGI_SCHEME'] == 'http' and env['SERVER_PORT'] == '80') or (env['UWSGI_SCHEME'] == 'https' and env['SERVER_PORT'] == '443'):
        return env['UWSGI_SCHEME']+'://'+env['SERVER_NAME']
    else:
        return env['UWSGI_SCHEME']+'://'+env['SERVER_NAME']+':'+env['SERVER_PORT']
