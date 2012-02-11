from bottle import PluginError, request, response, HTTPResponse

class BasicAuthPlugin(object):
    '''Plugin implementing Basic HTTP Authentication.'''

    name = 'basicauth'
    api = 2
    auth_header = [('WWW-Authenticate', 'Basic')]

    def __init__(self, users, max_auth_tries=3):
        '''
        :param users: dict user names as keys and passwords as values
        :param max_auth_tries: maximum number of auth attempts after
                               which IP will be added to list of banned.
                               If None then user cant be banned, default=3
        '''
        if not users:
            raise ValueError()
        self.users = users
        self.banned = []
        self.max_auth_tries = max_auth_tries
        self.failed_logins = {}

    def setup(self, app):
        for other in app.plugins:
            if isinstance(other, BasicAuthPlugin):
                raise PluginError('Another BasicAuthPlugin is installed')

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            ip = request.remote_addr
            if ip in self.banned:
                raise HTTPResponse(status=403)
            if request.auth is None:
                raise HTTPResponse(status=401,
                                   header=self.auth_header)
            user, password = request.auth
            if not user or not password:
                raise HTTPResponse(status=401,
                                   header=self.auth_header)
            if user not in self.users or password != self.users[user]:
                if self.max_auth_tries is not None:
                    if ip in self.failed_logins:
                        self.failed_logins[ip] += 1
                    else:
                        self.failed_logins[ip] = 1
                    if self.failed_logins[ip] >= self.max_auth_tries:
                        self.banned.append(ip)
                        del self.failed_logins[ip]
                        raise HTTPResponse(status=403)
                raise HTTPResponse(status=401,
                                   header=self.auth_header)
            if ip in self.failed_logins:
                del self.failed_logins[ip]
            return callback(*args, **kwargs)
        return wrapper

Plugin = BasicAuthPlugin
