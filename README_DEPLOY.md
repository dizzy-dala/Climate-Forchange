Deployment checklist for Climate Forchange

1. Ensure environment variables are set on the host:
   - DJANGO_SECRET_KEY
   - OPENWEATHER_API_KEY
   - DJANGO_DEBUG=False
   - DJANGO_ALLOWED_HOSTS=yourdomain.com

2. Install dependencies and collect static:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

3. Create a superuser if needed:

```bash
python manage.py createsuperuser
```

4. Render (or other) specific notes:
   - Add `Procfile` (already included) - Render will use it to start Gunicorn.
   - Ensure `staticfiles/` and `media/` are writable by the app.

5. Security:
   - Use HTTPS (Render provides TLS by default).
   - Keep secret values out of git and rotate keys when needed.

