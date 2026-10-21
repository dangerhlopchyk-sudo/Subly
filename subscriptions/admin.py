from django.contrib import admin
from .models import Category, Payment, Subscription, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "user")
    search_fields = ("name", "user__username")
    list_filter = ("user",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__username")
    list_filter = ("user",)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "price", "billing_cycle", "next_payment_date", "status", "auto_renew")
    list_filter = ("status", "billing_cycle", "category", "auto_renew")
    search_fields = ("name", "user__username")
    filter_horizontal = ("tags",)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("subscription", "amount", "paid_date", "note")
    list_filter = ("paid_date",)
    search_fields = ("subscription__name", "note")
    date_hierarchy = "paid_date"
