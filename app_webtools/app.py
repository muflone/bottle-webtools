# Import standard modules
import StringIO
import json

# Import third party modules
from beaker.middleware import SessionMiddleware
import bottle

# Import local modules
import configuration
from app_constants import (DIR_STATIC,
                           DIR_BEAKER_CACHE,
                           DIR_BEAKER_LOCKS,
                           SESSION_TIMEOUT)
from .constants import MODULE_NAME
from .requests import *


class BottleApplication(bottle.Bottle):
    def __init__(self):
        super(self.__class__, self).__init__()

        def serve_object_page(oPage):
            return self.handle_response(oPage.serve())

        @self.route('/static/<filepath:path>')
        def serve(filepath):
            """Serve the static files (resources)"""
            return self.handle_response('STATIC:%s:%s' % (
                filepath, configuration.get_path(MODULE_NAME, DIR_STATIC)))

        @self.route('/')
        def serve():
            """Serve the page"""
            return self.handle_response('REDIRECT:commands')

        @self.post('/login')
        @self.route('/login')
        def serve():
            """Serve the login page"""
            return serve_object_page(RequestLogin())

        @self.route('/logout')
        def serve():
            """Serve the login page"""
            return serve_object_page(RequestLogout())

        @self.route('/commands')
        @self.post('/commands')
        def serve():
            """Serve the page"""
            return serve_object_page(RequestCommands())

        @self.route('/folders')
        @self.post('/folders')
        def serve():
            """Serve the page"""
            return serve_object_page(RequestFolders())

        @self.route('/run')
        @self.post('/run')
        def serve():
            """Serve the page"""
            return serve_object_page(RequestRun())

    def handle_response(self, response):
        """Handle both responses and redirects"""
        # Always close the connection after the request
        bottle.response.set_header('Connection', 'close')
        if type(response) is bottle.HTTPResponse:
            # Direct HTTP response like a static file already served
            # (shouldn't happen)
            return response
        elif isinstance(response, StringIO.StringIO):
            # Direct StringIO response like a static file already served
            return response
        elif type(response) is dict:
            # Direct dictionary response
            return response
        elif type(response) is list:
            # Direct list response
            return json.dumps(response)
        elif response.startswith('REDIRECT:'):
            # Redirect to another page
            bottle.redirect(response[9:])
            return
        elif response.startswith('STATIC:'):
            # Static file served without the download option
            name, path = response[7:].split(':', 1)
            return bottle.static_file(name, root=path)
        elif response.startswith('DOWNLOAD:'):
            # Static file served with the download option
            name, path = response[9:].split(':', 1)
            return bottle.static_file(name, root=path, download=name)
        elif response.startswith('ABORT:'):
            # Error page
            code, message = response[6:].split(':', 1)
            bottle.abort(int(code), message)
        elif response.startswith('ERROR:'):
            # Error page without format
            code, message = response[6:].split(':', 1)
            return bottle.HTTPResponse(message, int(code))
        elif response.startswith('CSV:'):
            bottle.response.set_header('Content-Type', 'text/csv')
            return response[4:]
        elif response.startswith('TEXT:'):
            bottle.response.set_header('Content-Type', 'text/plain')
            return response[5:]
        else:
            return response


def setup():
    """Initial setup, called during the application mount"""
    # Create a new application
    session_opts = {
            'session.type': 'file',
            'session.cookie_expires': True,
            'session.data_dir': DIR_BEAKER_CACHE,
            'session.lock_dir': DIR_BEAKER_LOCKS,
            'session.auto': True,
            'session.timeout': SESSION_TIMEOUT,
            'session.secret': None,
            'session.encrypt_key': False,
            'session.validate_key': False,
            'session.invalidate_corrupt': True,
    }

    app = SessionMiddleware(
            BottleApplication(),
            config=session_opts,
            environ_key='beaker.session',
            key='beaker.session.id')
    return app
