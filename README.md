This is a simple url shortener I wrote more than anything to see if I could.
I am putting it out here in case anyone finds it of use.

pyURLShortener

https://github.com/korylprince/pyURLShortener

#Installing#

This will probably run on anything that will run uwsgi, but my particular setup uses nginx on Ubuntu.

I have included some configs to get you going.

If you are on ubuntu, install the uwsgi-python, python-memcache, memcached, and nginx packages, then put nginx.conf at /etc/nginx/sites-enabled/default and url.ini at /etc/uwsgi/apps-enabled/url.ini.

I placed url.py at /var/www/url/url.py, but you can put it where ever you want as long as you modify your uwsgi config to point to that spot.

There are two different modes you can use. If you can use the whole domain (to save space) you submit urls to /in/.
Otherwise submit them to /i/ and get them out as /o/. See Usage for more details.

A previous version used sqlite3 instead of memcached. To use this version download this repo and run git checkout a3616b32c647eb9c3ffe08933f1f0a9f160d0e37 .

#Usage#

Once you get it up and going, the usage is simple.

Requests to http(s)://yoursite.com/i/url
will return a plain text url of the form http(s)://yoursite.com/o/code, where code is 4 random characters.

Requests to http(s)://yoursite.com/in/url
will return a plain text url of the form http(s)://yoursite.com/code, where code is 4 random characters.

For example a request to http://yoursite.com/i/http://google.com/
would return the text http://yoursite.com/o/aZ2b.
Going to that URL would redirect you to http://google.com/.

Another example is a request to http://yoursite.com/in/http://google.com/
would return the text http://yoursite.com/aBg4.
Going to that URL would redirect you to http://google.com/.

#Caveats#

This is a simple project. There are no restrictions on what is put into memcached. 

I tried to account for different server addresss/ports/etc but I didn't actually test it so your mileage may vary.

Bottom Line, there's probably better stuff out there for you to use. If you want to change something or make it better, fork me.

#License#

This code is Public Domain. Do whatever you want. It'd be nice if you sent me an email telling me someone used it though.
