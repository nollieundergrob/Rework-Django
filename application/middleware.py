from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
import logging

logger = logging.getLogger('jwt_auth')

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        try:
            # Аутентификация только если токен предоставлен
            auth_result = self.jwt_authenticator.authenticate(request)
            if auth_result:
                user, token = auth_result
                request.user = user
        except AuthenticationFailed as e:
            logger.warning(f"Authentication failed: {e}")
            return JsonResponse({"error": "Invalid or expired token"}, status=401)
        except Exception as e:
            logger.error(f"Unexpected authentication error: {e}")
            return JsonResponse({"error": f"Authentication error:\n{e}"}, status=400)

        return self.get_response(request)
