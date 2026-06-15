from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

from .models import WeatherRequestLog


class MonitoringMiddleware(MiddlewareMixin):
    """Simple middleware to log weather page requests for monitoring."""

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            path = request.path or ''
            if path.startswith('/weather') and request.method.upper() == 'GET':
                city = request.GET.get('city', '')
                ip = request.META.get('REMOTE_ADDR', '') or request.META.get('HTTP_X_FORWARDED_FOR', '')
                user = request.user if request.user.is_authenticated else None
                # Summarize a short result if available from session
                result_summary = ''
                if hasattr(request, 'session'):
                    # session might store last weather summary under 'last_weather_summary'
                    result_summary = request.session.get('last_weather_summary', '')
                WeatherRequestLog.objects.create(
                    user=user,
                    city=city,
                    ip=ip,
                    result_summary=result_summary,
                )
        except Exception:
            # Avoid crashing requests on logging errors
            pass
        return None
