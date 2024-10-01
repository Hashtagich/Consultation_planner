#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#python3 manage.py flush --no-input
python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear

# Проверка существования суперпользователя
# Проверка существования суперпользователя
#if python3 manage.py shell -c "from users.models import CustomUser; print(CustomUser.objects.filter(is_superuser=True, email='$SUPERUSER_EMAIL').exists())" | grep -q True; then
#    echo "Superuser already exists"
#else
#    # Создание суперпользователя
#    echo "Creating superuser..."
#    python3 manage.py createsuperuser --noinput --email "$SUPERUSER_EMAIL" --middle_name "$SUPERUSER_MIDDLE_NAME" --first_name "$SUPERUSER_FIRST_NAME" --password "$SUPERUSER_PASSWORD"
#fi

exec "$@"