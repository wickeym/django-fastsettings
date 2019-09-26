# FastSettings

:Version: 0.4
:Download: <https://pypi.org/project/django-fastsettings>
:Source: <https://github.com/wickeym/django-fastsettings>
:Keywords: django, redis, database, settings, fastsettings

Django FastSettings stores settings in the database and syncs it to redis, so that access is "fast". This will work without redis, it will simply fetch from the database each time.

## Quick start

* `pip install django-fastsettings`

* Add "fastsettings" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'fastsettings',
    ]

* Add the Redis connection settings to the django settings.py file

    ``` python
    # PROJECT SETTINGS (used in fastsettings)
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = "your_redis_password"
    ```

* For logging, add a handler for "fastsettings_logger" in your logging configuration:

* Run `python manage.py migrate` to create the fastsettings models.

* Start the development server and visit <http://127.0.0.1:8000/admin/> to create a fastsetting (you'll need the Admin app enabled).
