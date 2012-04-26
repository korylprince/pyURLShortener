#!/usr/bin/python

"""
Simple url shortener.
Requests to host/i/http://site/
returns a code.
requests to host/o/code
redirects to http://site/

Requests to host/in/http://site/
returns a code.
requests to host/code
redirects to http://site/
"""
import memcache
import string
import random
import sqlite3
import os


def application(env, start_response):
    """
    main application
    """
    # get input
    request = env['REQUEST_URI']
    # if putting with subfolder
    if '/i/' in request:
        # start return
        start_response('200 OK', [('Content-Type','text/plain')])

        # generate code
        code = setURL(request[3:],env)
        if code == None:
            return "error"

        # send back code
        return getURLBase(env)+'/o/'+code

    # if putting no subfolder
    elif '/in/' in request:
        # start return
        start_response('200 OK', [('Content-Type','text/plain')])

        # generate code
        code = setURL(request[4:],env)
        if code == None:
            return "error"

        # send back code
        return getURLBase(env)+'/'+code
    
    # if getting subfolder
    elif '/o/' in request:

        url = getURL(request[3:],env)

        # check that code existed
        if url == None:
            start_response('200 OK', [('Content-Type','text/html')])
            return '<h1>URL Not Found</h1>'

        # we do have a code for it
        start_response('301 Moved Permanently', [('Location',url)])
        return 0

    # if getting no subfolder
    else:

        url = getURL(request[1:],env)

        # check that code existed
        if url == None:
            start_response('200 OK', [('Content-Type','text/html')])
            return '<h1>URL Not Found</h1>'

        # we do have a code for it
        start_response('301 Moved Permanently', [('Location',url)])
        return 0

def getURL(code, env):
    """
    Wrapper to check if code is in memcache
    then sqlite3
    """

    # connect to memcache and check for code
    mc = memcache.Client(['127.0.0.1:11211'])
    url = mc.get(code)

    # see if code exists
    if url != None:
        return url

    # make sure database file exists and table exists
    makeDB(env)

    # connect to database
    conn = sqlite3.connect(env['DOCUMENT_ROOT']+'/url.db')
    c = conn.cursor()


    # check if row in database
    c.execute('select url,code from url where code=?;',[code])
    row = c.fetchone()

    # check if there was a row
    if row != None:
        # add it back to memcached
        mc.set(row[1].encode('ascii'),row[0].encode('ascii'))
        return row[0]

    # nothing was found
    return None

def setURL(url,env):
    """
    Wrapper to generate code, add it to 
    memcached and sqlite3, then return it
    """
    
    # connect to memcached
    mc = memcache.Client(['127.0.0.1:11211'])

    # generate code
    char_set = string.letters+string.digits
    code = ''.join(random.sample(char_set,6))

    # make sure database file exists and has table
    makeDB(env)

    # connect to database
    conn = sqlite3.connect(env['DOCUMENT_ROOT']+'/url.db')
    c = conn.cursor()


    # check if row in database
    c.execute('select code from url where code=?;',[code])
    row = c.fetchone()

    # make sure code is not in memcached or sqlite
    while mc.get(code) != None or row != None:
        # generate new code and run query again
        code = ''.join(random.sample(char_set,6))
        c.execute('select code from url where code=?;',[code])
        row = c.fetchone()

    # add url to sqlite
    c.execute('insert into url(code,url) values(?,?);',[code,url])

    # Get row just set
    c.execute('select code from url where code=?;',[code])
    row = c.fetchone()

    # make sure added to sqlite
    if row == None:
        return None 

    # commit to database and close
    conn.commit()
    conn.close()    

    # add to memcached
    mc.set(code,url)

    return code

def getURLBase(env):
    """
    returns http(s)://server(:port) part of url
    """
    if (env['UWSGI_SCHEME'] == 'http' and env['SERVER_PORT'] == '80') or (env['UWSGI_SCHEME'] == 'https' and env['SERVER_PORT'] == '443'):
        return env['UWSGI_SCHEME']+'://'+env['SERVER_NAME']
    else:
        return env['UWSGI_SCHEME']+'://'+env['SERVER_NAME']+':'+env['SERVER_PORT']

def makeDB(env):
    """
Sets up db
"""
    conn = sqlite3.connect(env['DOCUMENT_ROOT']+'/url.db')
    c = conn.cursor()
    c.execute('create table if not exists url(code varchar(10) primary key, url longtext);')
    conn.commit()
    conn.close()
