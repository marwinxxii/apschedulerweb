================
Bottle-BasicAuth
================

This plugin adds HTTP Basic authentication to Bottle application.

Usage
=====

:class:`BasicAuthPlugin` object accepts dict with usernames as keys and
passwords as values. Also maximum number of authorization tries can be
passed as keyword argument.::
    import bottle
    
    app = bottle.Bottle()
    plugin = bottle.ext.basicauth.Plugin({'user': 'pass'})
    app.install(plugin)
    
    @app.route('/')
    def index():
    	pass

Configuration
=============

Beside the ``users`` argument, there is a ``max_auth_tries`` which is a
maximum number of authorization attempts for user. if it is not None, than
after this number of authorization failures user's IP will be added to list
of banned.
