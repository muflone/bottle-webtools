# Import standard modules
import hashlib

# Import local modules
from .base import AuthenticatorBase


class AuthenticatorSHA512(AuthenticatorBase):
    ALGORITHM = 'sha512'

    def __init__(self, db_settings):
        super(self.__class__, self).__init__(db_settings)

    def check_login(self, username, password):
        super(self.__class__, self).check_login(username, password)
        return self.check_password(username,
                                   hashlib.sha512(password).hexdigest())
