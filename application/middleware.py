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
        logger.debug(f"Request path: {request.path}, Method: {request.method}")
        if request.path in ['/auth/login/', '/users/']:
            return self.get_response(request)

        try:
            user, token = self.jwt_authenticator.authenticate(request)
            if user:
                request.user = user
                logger.info(f"Authenticated user: {user.username}")
        except AuthenticationFailed as e:
            logger.warning(f"Authentication failed: {e}")
            return JsonResponse({"error": "Invalid or expired token"}, status=401)
        except Exception as e:
            logger.error(f"Unexpected authentication error: {e}")
            return JsonResponse({"error": "Authentication error"}, status=400)

        return self.get_response(request)



class LogAllRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        logger.info(f"Response: {response.status_code} for {request.method} {request.path}")
        return response
