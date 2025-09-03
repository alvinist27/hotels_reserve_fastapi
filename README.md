docker run --name hotels_db \
    -p 5432:5432 \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=booking \
    --network=HotelsNetwork \
    --volume=pg-hotels-data:/var/lib/postgresql/data \
    -d  postgres:16

docker run --name redis \
    -p 6379:6379 \
    --network=HotelsNetwork \
    -d redis:7.4

docker run --name hotels_reserve_celery_worker \
    --network=HotelsNetwork \
    hotels \
    celery -A src.tasks.celery_app:celery_instance worker -l INFO

docker run --name hotels_reserve_celerybeat_worker \
    --network=HotelsNetwork \
    hotels \
    celery -A src.tasks.celery_app:celery_instance beat -l INFO

docker run --name hotels_reserve \
    -p 8080:8080 \
    --network=HotelsNetwork \
    hotels

docker run --name hotels_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --volume /etc/letsencrypt:/etc/letsencrypt \
    --volume /var/lib/letsencrypt:/var/lib/letsencrypt \
    --network=HotelsNetwork \
    -p 80:80 -d nginx
