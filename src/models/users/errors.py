__author__ = 'hooper-p'

class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistsError(UserError):
    pass


class IncorrectPasswordError(UserError):
    pass


class UserAlreadyRegisteredError(UserError):
    pass


class PasswordsNotMatch(UserError):
    pass


class PasswordStrength(UserError):
    pass


class ResetPasswordWrongUser(UserError):
    pass


class AdminCreatedUserError(UserError):
    pass