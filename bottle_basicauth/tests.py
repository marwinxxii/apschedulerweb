import unittest
import base64

from bottle.ext import basicauth
from tools import ServerTestBase

class TestBasicAuth(ServerTestBase):
    
    users = {'user': 'pass'}

    def setUp(self):
        ServerTestBase.setUp(self)
        self.plugin = self.app.install(basicauth.Plugin(self.users))
        self.app.catchall = False
        @self.app.route('/')
        def test():
            pass

    def test_asks_auth(self):
        result = self.urlopen('/')
        header = result['header'].get('Www-Authenticate')
        self.assertEqual(result['code'], 401)
        self.assertEqual(header, 'Basic')

    def test_auth_pass(self):
        userpass = base64.b64encode('%s:%s' % self.users.items()[0])
        env = {'HTTP_AUTHORIZATION': 'Basic %s' % userpass}
        self.assertStatus(200, '/', env=env)

    def test_bans(self):
        userpass = 'Basic %s' % base64.b64encode('pass:user')
        for i in range(self.plugin.max_auth_tries):
            self.urlopen('/', env={'HTTP_AUTHORIZATION': userpass})
        self.assertStatus(403, '/')

if __name__ == '__main__':
    unittest.main()
