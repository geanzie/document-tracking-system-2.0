from datetime import timedelta
from django.utils.timezone import now

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                elapsed_time = now() - last_activity
                if elapsed_time > timedelta(minutes=5):
                    from django.contrib.auth import logout
                    logout(request)
            request.session['last_activity'] = now()
        return self.get_response(request)
