flask db upgrade
gunicorn -b :$PORT "app:create_app()"