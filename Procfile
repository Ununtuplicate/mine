release: yes "yes" | python manage.py migrate
web: uwsgi --http-socket=:$PORT --master --workers=2 --threads=8 --die-on-term --wsgi-file=mine/wsgi.py  --static-map /media/=/app/mine/media/ --offload-threads 1
