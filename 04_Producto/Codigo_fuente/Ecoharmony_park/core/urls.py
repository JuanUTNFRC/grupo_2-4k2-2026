from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from apps.inscripciones.views import InscripcionView

urlpatterns = [
    path('', InscripcionView.as_view(), name='inscripcion'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('api/', include('apps.actividades.urls')),
    path('api/', include('apps.inscripciones.urls')),
]
