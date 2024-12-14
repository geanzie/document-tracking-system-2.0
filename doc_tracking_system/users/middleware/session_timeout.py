# users/middleware/session_timeout.py
import time
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the session timeout is configured and if the user is logged in
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            current_time = time.time()
            if last_activity and (current_time - last_activity) > settings.SESSION_TIMEOUT:
                logout(request)
                return redirect('login')  # Redirect to login after session expiration

            # Update last activity time in session
            request.session['last_activity'] = current_time

        response = self.get_response(request)
        return response
