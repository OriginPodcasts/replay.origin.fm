from django.urls import path
from .views import CookiesView, PrivacyView


urlpatterns = (
    path('cookies/', CookiesView.as_view(), name='cookies'),
    path('privacy/', PrivacyView.as_view(), name='privacy')
)
