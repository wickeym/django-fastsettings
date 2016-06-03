from django.contrib import admin
import fastsettings.models


# Register your models here.
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'action_int','action_str', 'use_integer', 'use_string', 'description', 'game_name')
    list_filter = ('use_integer', 'use_string', 'game_name', )
    search_fields = ('name', 'action_int', 'action_str', 'description', )

admin.site.register(fastsettings.models.Settings, SettingsAdmin)