from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("subscriptions/", views.SubscriptionListView.as_view(), name="list"),
    path("subscriptions/add/", views.SubscriptionCreateView.as_view(), name="add"),
    path("subscriptions/<int:pk>/", views.SubscriptionDetailView.as_view(), name="detail"),
    path("subscriptions/<int:pk>/edit/", views.SubscriptionUpdateView.as_view(), name="edit"),
    path("subscriptions/<int:pk>/delete/", views.SubscriptionDeleteView.as_view(), name="delete"),
    path("subscriptions/<int:pk>/paid/", views.subscription_paid, name="paid"),
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("categories/add/", views.CategoryCreateView.as_view(), name="category_add"),
    path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("categories/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category_delete"),
    path("tags/", views.TagListView.as_view(), name="tags"),
    path("tags/add/", views.TagCreateView.as_view(), name="tag_add"),
    path("tags/<int:pk>/", views.TagDetailView.as_view(), name="tag_detail"),
    path("tags/<int:pk>/delete/", views.TagDeleteView.as_view(), name="tag_delete"),
    path("payments/", views.PaymentListView.as_view(), name="payments"),
    path("payments/<int:pk>/", views.PaymentDetailView.as_view(), name="payment_detail"),
    path("manager/", views.ManagerOverviewView.as_view(), name="manager_overview"),
]
