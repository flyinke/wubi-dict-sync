from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .token_utils import TokenUtils

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        uid = request.headers.get('diary-uid')
        token = request.headers.get('diary-token')

        if not uid or not token:
            return None

        user = TokenUtils.verify_token(token)

        if not user:
            raise AuthenticationFailed('Invalid or expired token.')

        if user.id != int(uid):
            raise AuthenticationFailed('User ID does not match token.')

        return (user, token)
