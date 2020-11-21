release: python manage.py migrate
web: gunicorn mdb.wsgi:application --log-file -