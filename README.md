This is a simple url shortener I wrote more than anything to see if I could.
I am putting it out here in case anyone finds it of use.

It uses memcached and sqlite3 to store urls and serve them back as fast as possible whle retaining data.

pyURLShortener

https://github.com/korylprince/pyURLShortener

#Installing#

This will probably run on anything that will run uwsgi, but my particular setup uses nginx on Ubuntu.

I have included some configs to get you going.

If you are on ubuntu, install the uwsgi-python (uwsgi and uwsgi-plugin-python on newer versions of ubuntu), python-memcache, python-sqlite, memcached, and nginx packages, then put nginx.conf at /etc/nginx/sites-enabled/default and url.ini at /etc/uwsgi/apps-enabled/url.ini.

I placed url.py at /var/www/url/url.py, but you can put it where ever you want as long as you modify your uwsgi and nginx (for document root) config to point to that spot.

There are two different modes you can use. If you can use the whole domain (to save character space) you submit urls to /in/.
Otherwise submit them to /i/ and get them out as /o/. See Usage for more details.

There are two notable previous versions:

git checkout 721ecfe1ba5191d48043e85fa53af21315bce57c

Will give you a url.py that only uses memcached (will be faster but you will lose url data eventually.)

git checkout a3616b32c647eb9c3ffe08933f1f0a9f160d0e37

Will give you a url.py that uses only sqlite3 (will be slower.)

#Usage#

Once you get it up and going, the usage is simple.

Requests to http(s)://yoursite.com/i/url
will return a plain text url of the form http(s)://yoursite.com/o/code, where code is 6 random characters.

Requests to http(s)://yoursite.com/in/url
will return a plain text url of the form http(s)://yoursite.com/code, where code is 6 random characters.

For example a request to http://yoursite.com/i/http://google.com/
would return the text http://yoursite.com/o/aZ2bB1.
Going to that URL would redirect you to http://google.com/.

Another example is a request to http://yoursite.com/in/http://google.com/
would return the text http://yoursite.com/aBg43R.
Going to that URL would redirect you to http://google.com/.

#Caveats#

This is a simple project. There are no restrictions on what is put into the databases (except for simple anti-sql-injection.) 

I have tested this on a few different server configurations, but I can't promise it will work. If you'd like help, shoot me an email

Bottom Line, there's probably better stuff out there for you to use. If you want to change something or make it better, fork me.

#License#

Code is Copyright 2012 Kory Prince (korylprince at gmail dot com)
This code is Public Domain. There is no warranty. Do whatever you want. It'd be nice if you sent me an email telling me someone used it though.
