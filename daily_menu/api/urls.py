from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken import views

from api.routers import router
from api.viewsets import RegistrationView, PasswordResetView, SearchView

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/login/', views.obtain_auth_token),
    path('v1/registration/', csrf_exempt(RegistrationView.as_view())),
    path('v1/reset_password/', csrf_exempt(PasswordResetView.as_view())),
]
