export FLASK_APP=run.py
flask db upgrade
gunicorn -b :$PORT app:app