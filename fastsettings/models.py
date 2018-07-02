# -*- encoding=UTF-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from . import projectsettings as fstsettings
import logging

logger = logging.getLogger('fastsettings_logger')


class Settings(models.Model):
    # Common Settings #
    # ==========Fields============== #
    # Utility name #
    name = models.CharField(primary_key=True, max_length=64, help_text="Name of setting, must be unique.")
    # Can be used for anything. (name='version' Current version of the app) #
    action_int = models.IntegerField(blank=True, null=True,
                                     help_text="The setting integer. NOTE: If only using integer, check use_integer box and uncheck use_string!")
    # Can be used for anything. #
    action_str = models.TextField(blank=True, null=True,
                                  help_text='The setting string. (json: {"key:"val","key2":2}) NOTE: If only using string, check use_string box and uncheck use_integer!')
    # Use integer part of this setting? #
    use_integer = models.BooleanField(default=True, help_text="Use integer part of this setting?")
    # Use string part of this setting? #
    use_string = models.BooleanField(default=False, help_text="Use string part of this setting?")
    # Description of setting. #
    description = models.CharField(blank=True, null=True, max_length=200, help_text="Description of setting.")
    # Game Name #
    game_name = models.CharField(default="testapp", max_length=12)

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"
        app_label = "fastsettings"


# ==================================== #
# Handle save signals.
# e.g. When Settings gets saved, re-sync
# the settings key in redis.
# Redis is used to so the db isn't hit
# as often.
# ==================================== #
@receiver(post_save, sender=Settings)
def on_settings_save(sender, **kwargs):
    settingobj = kwargs.get('instance', None)
    if (settingobj is not None):
        the_setting = None
        try:
            # Update setting entry
            settings_name = "{0}_PROJECT_SETTINGS".format(fstsettings.get_from_settings_file("APP_NAME", ""))
            the_setting = {'action_int': settingobj.action_int, 'action_str': settingobj.action_str,
                           'use_integer': settingobj.use_integer, 'use_string': settingobj.use_string}
            the_setting = json.dumps(the_setting)
            redis_settings_server = fstsettings.get_redis_connection()
            redis_settings_server.hset(settings_name, settingobj.name, the_setting)
        except Exception as e:
            logger.error("on_settings_save: setting_obj:{0}".format(the_setting), exc_info=e)
