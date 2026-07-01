from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
#from django.views.generic import RedirectView


urlpatterns = ([
    path('admin/', admin.site.urls),
    path('authuser/', include('authuser.urls')),
    path('', include('base.urls')),
    path('doctor/', include('doctor.urls')),
    path('pacient/', include('pacient.urls')),

    # path('', RedirectView.as_view(pattern_name='authuser:sign-up', permanent=False)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
               static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))


