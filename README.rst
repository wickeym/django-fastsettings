=====
FastSettings
=====

Django FastSettings stores settings in the database and syncs it to redis, so that access is "fast". 
This will work without redis, it will simply fetch from the database each time.

Quick start
-----------

1. Add "fastsettings" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'fastsettings',
    ]

2. Add the Redis connection settings to the django settings.py file
# PROJECT SETTINGS (used in fastsettings) # 
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = "your_redis_password"

3. For logging, add a handler for "fastsettings_logger" in your logging configuration::

4. Run `python manage.py migrate` to create the fastsettings models.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a fastsettings (you'll need the Admin app enabled).
