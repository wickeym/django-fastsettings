# -*- encoding=UTF-8 -*-
'''
This module will provide access to any project wide settings/globals, that are stored in the settings table in the database.
The settings may be in cache or db, to provide a single get/set, this module will provide the intermediary functions.

Created on Jul 9, 2014

@author: michael wickey
'''
from __future__ import unicode_literals
from django.conf import settings
import json
import redis
import logging
logger = logging.getLogger('fastsettings_logger')

REDIS_CONN = None


def get_redis_connection():
    global REDIS_CONN
    try:
        if(REDIS_CONN is None):
            REDIS_CONN = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD)
    except Exception as e:
        logger.error("get_redis_connection:", exc_info=e)
    return REDIS_CONN


def get_from_settings_file(settingname, defaultval=None, the_logger=logger):
    ret_val = None
    try:
        ret_val=getattr(settings, settingname, None)
        if(ret_val is None):
            ret_val = defaultval
            the_logger.warning("Setting:{0} not found in settings.py, used default:{1}".format(settingname, defaultval))
    except Exception as e:
        ret_val = defaultval
        logger.error("[get_from_settings_file] setting:{0}, used default:{1}. Error: {2}".format(settingname, ret_val, e), exc_info=e)
    return ret_val


def get_values(thesetting):
    ret_val = None
    if(thesetting['use_integer'] and thesetting['use_string']):
        ret_val = {'action_int': thesetting['action_int'], 'action_str': thesetting['action_str']}
    elif(thesetting['use_integer']):
        ret_val = thesetting['action_int']
    elif(thesetting['use_string']):
        ret_val = thesetting['action_str']
    return ret_val


def get_from_settings_db(settingname, defaultval=None, the_logger=logger):
    ret_val = None
    import fastsettings.models as models
    try:
        settings_name = "{0}_PROJECT_SETTINGS".format(get_from_settings_file("APP_NAME", ""))
        redis_settings_server = get_redis_connection()
        if(redis_settings_server is not None):
            ret_val = redis_settings_server.hget(settings_name, settingname)
        if(ret_val is None):
            the_setting = models.Settings.objects.get(name=settingname)
            ret_val = {'action_int': the_setting.action_int, 'action_str': the_setting.action_str, 'use_integer': the_setting.use_integer, 'use_string': the_setting.use_string}
            ret_val = get_values(ret_val)
            the_logger.warning("Setting:{0} not found in Redis, retrieved from database".format(settingname))
        else:
            ret_val = json.loads(ret_val)
            ret_val = get_values(ret_val)
            
    except models.Settings.DoesNotExist:
        ret_val = defaultval
        the_logger.warning("Setting:{0} not found in Redis/database, used default:{1}".format(settingname, defaultval))
    except Exception as e:
        ret_val = defaultval
        logger.error("[get_from_settings_db] setting:{0}, used default:{1}. Error: {2}".format(settingname, ret_val, e), exc_info=e)
        
    return ret_val


