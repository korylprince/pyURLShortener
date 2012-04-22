#!/usr/bin/python

"""
Simple url shortener.
Requests to host/i/http://site/
returns a code.
requests to host/o/code
redirects to http://site/
"""
import sqlite3
import os.path


def application(env, start_response):
    """
    main application
    """
    # get input
    request = env['REQUEST_URI']
    # check to make sure db is there again
    if not os.path.exists(env['DOCUMENT_ROOT']+'/url.db'):
        makeDB(env)
    # open sqlite3
    conn = sqlite3.connect(env['DOCUMENT_ROOT']+'/url.db')
    c = conn.cursor()
    # if inputing
    if '/i/' in request:
        # See if it's already there
        c.execute('select code from url where url=?;',[request[3:]])
        row = c.fetchone()
        # if not put it there
        if row == None:
            c.execute('insert into url(url) values(?);',[request[3:]]) 
            conn.commit()
            c.execute('select code from url where url=?;',[request[3:]])
            row = c.fetchone()
        conn.close()
        # send back code
        start_response('200 OK', [('Content-Type','text/plain')])
        return getURLBase(env)+'/o/'+str(row[0])
    
    # if getting
    elif '/o/' in request:
        c.execute('select url from url where code=?;',[request[3:]])
        row = c.fetchone()
        conn.close()
        # if we don't have a code for it
        if row == None:
            start_response('200 OK', [('Content-Type','text/html')])
            return '<h1>URL Not Found</h1>'
        # we do have a code for it
        start_response('301 Moved Permanently', [('Location',str(row[0]))])
        return 0

    # something weird happened
    else:
        start_response('200 OK', [('Content-Type','text/html')])
        return '<h1>Error</h1>'

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
    c.execute('create table if not exists url(code integer primary key autoincrement, url varchar(200));')
    conn.commit()
    conn.close()
