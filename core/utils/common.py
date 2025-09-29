
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def generateToken(user):
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    return token
