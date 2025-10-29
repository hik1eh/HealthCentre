from django.contrib import admin

from .models import Pacient, Notification

class PacientAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'full_name',
                    'email',
                    'mobile',
                    'gender',
                    'dob')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('pacient',
                    'appointment',
                    'category',
                    'seen',
                    'date')
admin.site.register(Pacient, PacientAdmin)
admin.site.register(Notification, NotificationAdmin)