formidable - a simple form sending appliance
============================================

I wrote this little piece of python to have a simple POST request to email service without having to think too much.

Prerequisites
--------------

- python3
- [pipenv](https://docs.pipenv.org/)

Any python3 

What is it?
-------------

It's a little [flask](http://flask.pocoo.org/) application


Run it
-------

```
$ pipenv install
$ pipenv run FLASK_APP=formidable.py flask run
```

Configure
----------

I recommend to copy the `default.py` file in `config` and call it`local.py`. Adjust all configuration parameters to your needs. Refer to [flask documentation](http://flask.pocoo.org/docs/0.12/config/) and [flask-mail documentation](https://pythonhosted.org/Flask-Mail/) for additional information.

Set the env variable `FORMIDABLE_SETTINGS_MODULE` to `config.local` to have your config file applied.
```
$ export FORMIDABLE_SETTINGS_MODULE=config.local
```

Usage
------

The app exposes the `/submit` endpoint. Formdata sent there will be picked up and sent to your configured e-mail address.

Just create an HTML-Form similar to this:
```html
<form method="post" action="formidable.yourdomain.com/submit">
    <input type="text" name="name" placeholder="Your Name">
    <input type="text" name="message" placeholder="Type your message">
</form>
```

Deployment
-----------

For now no ready-made docker / heroku / vagrant or whatsoever deployment configuration. There are propably hundreds of ways of hosting a simple python application.

Here just an example what a uwsgi configuration on a debian 9 box could look like:

```ini
[uwsgi]
chdir = /var/www/apps/formidable
module = formidable:app
venv = /var/www/.local/share/virtualenvs/formidable-85KupQM6
master = true
processes = 2
uid = formidable
gid = formidable
plugins = python3
socket = /var/www/apps/formidable/formidable.sock
chmod-socket = 660
vacuum = true
```

The you might want to put a nginx proxy before that with a configuration like this:

```
server {
    server_name formidable.yourdomain.com;
    listen 80;
    listen [::]:80;
    location / {
        uwsgi_pass unix:/var/www/apps/formidable/formidable.sock;
        include uwsgi_params;
    }
}
```


Roadmap
--------

In this state it's just a little hacky thing, do not expect too much of it. Probably it will receive some kind of captcha integration.