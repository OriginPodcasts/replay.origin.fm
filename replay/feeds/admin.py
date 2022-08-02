from django.contrib import admin
from .models import Subscription, BlockedFeed


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('url', 'start_date', 'last_fetched')

    def has_add_permission(self, request):
        return False


@admin.register(BlockedFeed)
class BlockedFeedAdmin(admin.ModelAdmin):
    list_display = ('url',)
