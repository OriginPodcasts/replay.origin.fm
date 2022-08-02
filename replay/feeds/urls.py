from django.urls import path
from .views import (
    CreateSubscriptionView,
    SubscriptionDetialView,
    SubscriptionFeedView
)


urlpatterns = (
    path('subscribe/', CreateSubscriptionView.as_view(), name='create_subscription'),  # NOQA
    path('view/<uuid:pk>/', SubscriptionDetialView.as_view(), name='subscription_detail'),  # NOQA
    path('feeds/<uuid:pk>/', SubscriptionFeedView.as_view(), name='subscription_feed')  # NOQA
)
