This is a simple url shortener I wrote more than anything to see if I could.
I am putting it out here in case anyone finds it of use.

pyURLShortener
https://github.com/korylprince/pyURLShortener

#Installing#

This will probably run on anything that will run uwsgi, but my particular setup uses nginx on Ubuntu.

I have included some configs to get you going.

If you are on ubuntu, install the uwsgi-python, python-sqlite, and nginx packages, then put nginx.conf at /etc/nginx/sites-enabled/default and url.ini at /etc/uwsgi/apps-enabled/url.ini.

I placed url.py at /var/www/url/url.py, but you can put it where ever you want as long as you modify your nginx and uwsgi config to point to that spot.

The script will create a sqlite3 database on the first request in the directory defined by root in your nginx.conf, so your uwsgi will need write permissions there (www-data on ubuntu.)

#Usage#

Once you get it up and going, the usage is simple.

Requests to http(s)://yoursite.com/i/url
will return a plain text url of the form http(s)://yoursite.com/o/code, where code is some number.

For example a request to http://yoursite.com/i/http://google.com/
would return the text http://yoursite.com/o/5.
Going to that URL would redirect you to http://google.com/.

#Caveats#

This is a simple project. There are no restrictions on what is put into the database (basic anti-sql injection is done though.)

Your database may fill up and make things slower. This probably isn't real efficient. You can always just have a cron job remove the database though, as it will be automatically created.

I tried to account for different server address/ports/etc but I didn't actaully test it so your mileage may vary.

Bottom Line, there's probably better stuff out there for you to use. If you want to change something or make it better, fork me.

#License#

This code is Public Domain. Do whatever you want. It'd be nice if you sent me an email telling me someone used it though.
