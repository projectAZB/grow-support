from enum import Enum


class UserError(Enum):
    USERNAME_NOT_FOUND = 'No user with the username "{username}" in our database. Try Again.'
    INVALID_USERNAME_PASSWORD = 'Invalid username/password combination.'
    ACCOUNT_ALREADY_EXISTS = 'Account with username "{username}" already exists.'
