import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from collections import defaultdict

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

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store IPs and their timestamps of message sends
        self.message_log = defaultdict(list)
        self.TIME_WINDOW = 60  # in seconds
        self.MESSAGE_LIMIT = 5

    def __call__(self, request):
        # Only track POST requests to message endpoints
        if request.method == 'POST' and request.path.startswith('/api/messages'):
            ip = self.get_ip(request)
            current_time = time.time()

            # Remove timestamps older than 60 seconds
            self.message_log[ip] = [t for t in self.message_log[ip] if current_time - t < self.TIME_WINDOW]

            if len(self.message_log[ip]) >= self.MESSAGE_LIMIT:
                return HttpResponseForbidden("Message limit exceeded. Try again in a minute.")

            # Log the current timestamp
            self.message_log[ip].append(current_time)

        return self.get_response(request)

    def get_ip(self, request):
        # Handle reverse proxies if any
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check only for authenticated users
        if request.user.is_authenticated:
            user_role = getattr(request.user, 'role', None)

            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied. Admins or moderators only.")

        return self.get_response(request)
