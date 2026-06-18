from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render

from .forms import ProfileForm, UserRegistrationForm
from .models import NewsArticle, PDFResource, WeatherAlert, UserProfile
from .utils import get_weather_data
from .models import AuditLog, WeatherRequestLog
from django.http import HttpResponse, JsonResponse
import csv
import io
from django.views.decorators.http import require_GET


def home(request):
    news = NewsArticle.objects.filter(active=True).order_by('-published_at')[:4]
    alerts = WeatherAlert.objects.filter(active=True).order_by('-created_at')[:5]
    resources = PDFResource.objects.filter(active=True).order_by('-uploaded_at')[:3]
    return render(request, 'home.html', {'news': news, 'alerts': alerts, 'resources': resources})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration completed successfully.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})


def weather(request):
    city = request.GET.get('city', 'Nairobi')
    weather_data = get_weather_data(city=city)
    # store a short summary in session for monitoring middleware
    try:
        summary = ''
        if isinstance(weather_data, dict) and not weather_data.get('error'):
            summary = f"{weather_data.get('temperature')}C {weather_data.get('description')}"
        request.session['last_weather_summary'] = summary
    except Exception:
        pass
    return render(request, 'weather.html', {'weather': weather_data, 'city': city})


@require_GET
def weather_api(request):
    city = request.GET.get('city')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if lat and lon:
        try:
            lat_value = float(lat)
            lon_value = float(lon)
        except ValueError:
            return JsonResponse({'error': 'Invalid latitude or longitude.'}, status=400)
        weather_data = get_weather_data(lat=lat_value, lon=lon_value)
    elif city:
        weather_data = get_weather_data(city=city)
    else:
        return JsonResponse({'error': 'Please provide a city or coordinates.'}, status=400)

    if not weather_data.get('error'):
        WeatherRequestLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            city=weather_data.get('city') or city or '',
            ip=request.META.get('REMOTE_ADDR', ''),
            result_summary=f"{weather_data.get('temperature')}C {weather_data.get('description')}",
        )

    return JsonResponse(weather_data)


@login_required
def monitor(request):
    if not request.user.is_staff:
        messages.warning(request, 'Administrator access is required to view the monitor.')
        return redirect('home')

    recent_audits = AuditLog.objects.all()[:25]
    recent_weather = WeatherRequestLog.objects.all()[:50]
    stats = {
        'users': User.objects.count(),
        'news': NewsArticle.objects.count(),
        'resources': PDFResource.objects.count(),
        'alerts': WeatherAlert.objects.count(),
        'weather_requests': WeatherRequestLog.objects.count(),
    }
    return render(request, 'monitor.html', {'audits': recent_audits, 'weather_logs': recent_weather, 'stats': stats})


@login_required
@require_GET
def export_audits_csv(request):
    if not request.user.is_staff:
        messages.warning(request, 'Administrator access is required to export logs.')
        return redirect('home')

    qs = AuditLog.objects.all().order_by('-created_at')
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(['level', 'action', 'user', 'details', 'created_at'])
    for a in qs:
        writer.writerow([a.level, a.action, a.user.username if a.user else '', a.details, a.created_at.isoformat()])

    resp = HttpResponse(buf.getvalue(), content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="audit_logs.csv"'
    return resp


@login_required
@require_GET
def export_weather_csv(request):
    if not request.user.is_staff:
        messages.warning(request, 'Administrator access is required to export logs.')
        return redirect('home')

    qs = WeatherRequestLog.objects.all().order_by('-created_at')
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(['city', 'user', 'ip', 'result_summary', 'created_at'])
    for w in qs:
        writer.writerow([w.city, w.user.username if w.user else '', w.ip, w.result_summary, w.created_at.isoformat()])

    resp = HttpResponse(buf.getvalue(), content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="weather_requests.csv"'
    return resp


@login_required
@require_GET
def monitor_data(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'forbidden'}, status=403)

    # return simple counts and recent per-day weather request counts
    from django.utils import timezone
    from django.db.models import Count
    now = timezone.now()
    week_ago = now - timezone.timedelta(days=7)

    counts = WeatherRequestLog.objects.filter(created_at__gte=week_ago).extra({'day': "date(created_at)"}).values('day').annotate(cnt=Count('id')).order_by('day')
    data = {
        'counts': list(counts),
    }
    return JsonResponse(data)


def resources(request):
    query = request.GET.get('q', '')
    resources = PDFResource.objects.filter(active=True)
    if query:
        resources = resources.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'resources.html', {'resources': resources, 'query': query})


def news_list(request):
    articles = NewsArticle.objects.filter(active=True).order_by('-published_at')
    return render(request, 'news.html', {'articles': articles})


def alerts_list(request):
    alerts = WeatherAlert.objects.filter(active=True).order_by('-created_at')
    return render(request, 'alerts.html', {'alerts': alerts})


@login_required
def dashboard(request):
    if request.user.is_staff:
        counts = {
            'users': User.objects.count(),
            'resources': PDFResource.objects.count(),
            'news': NewsArticle.objects.count(),
            'alerts': WeatherAlert.objects.count(),
        }
        active_alerts = WeatherAlert.objects.filter(active=True).count()
        return render(request, 'dashboard.html', {'counts': counts, 'active_alerts': active_alerts})

    latest_alerts = WeatherAlert.objects.filter(active=True).order_by('-created_at')[:3]
    latest_news = NewsArticle.objects.filter(active=True).order_by('-published_at')[:3]
    resources = PDFResource.objects.filter(active=True).order_by('-uploaded_at')[:4]
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    weather_data = get_weather_data(city=profile.city or 'Nairobi')

    return render(request, 'dashboard.html', {
        'welcome_name': request.user.first_name or request.user.username,
        'weather_data': weather_data,
        'latest_alerts': latest_alerts,
        'latest_news': latest_news,
        'resources': resources,
        'profile': profile,
    })
