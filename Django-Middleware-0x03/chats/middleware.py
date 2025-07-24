import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)
handler = logging.FileHandler('user_requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response
        
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()

        restricted_start = time(18, 0, 0)
        restricted_end = time(21, 0, 0)

        if request.path.startswith('/api/messages') or request.path.startswith('/api/conversations'):
            if restricted_start <= now <= restricted_end:
                return HttpResponseForbidden("Access to messaging is restricted between 6 PM and 9 PM.")
                
        return self.get_response(request)
