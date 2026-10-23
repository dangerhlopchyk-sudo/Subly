import datetime
from decimal import Decimal
from math import pi

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .catalog import SERVICES, categories as catalog_categories, get_service
from .forms import CategoryForm, SubscriptionFilterForm, SubscriptionForm, TagForm
from .models import Category, Payment, Subscription, Tag

WEEKDAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
RING_RADIUS = 90
RING_LENGTH = 2 * pi * RING_RADIUS
RING_ARC = RING_LENGTH * 0.75


def _user_subs(user):
    return Subscription.objects.filter(user=user).select_related("category")


def _visible_categories(user):
    return Category.objects.filter(Q(user__isnull=True) | Q(user=user))


class QuerystringMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop("page", None)
        context["querystring"] = params.urlencode()
        return context


@login_required
def dashboard(request):
    today = datetime.date.today()
    subs = list(_user_subs(request.user))
    active = [s for s in subs if s.is_active]

    month_total = sum((s.monthly_cost for s in active), Decimal("0"))
    year_total = sum((s.yearly_cost for s in active), Decimal("0"))
    priciest = max(active, key=lambda s: s.monthly_cost, default=None)
    cheapest = min(active, key=lambda s: s.monthly_cost, default=None)

    paid_sum = sum(
        (s.price for s in subs if s.last_paid_date and s.last_paid_date.year == today.year
         and s.last_paid_date.month == today.month),
        Decimal("0"),
    )
    due_sum = sum(
        (s.price for s in active if (s.next_payment_date.year, s.next_payment_date.month)
         <= (today.year, today.month)),
        Decimal("0"),
    )
    share = float(paid_sum / (paid_sum + due_sum)) if (paid_sum + due_sum) else 0.0
    ring = {
        "circ": f"{RING_LENGTH:.2f}",
        "track": f"{RING_ARC:.2f}",
        "progress": f"{RING_ARC * share:.2f}",
        "percent": round(share * 100),
        "r": RING_RADIUS,
    }

    pay_days = {}
    for s in active:
        pay_days.setdefault(s.next_payment_date, []).append(s)
    strip = []
    for i in range(14):
        d = today + datetime.timedelta(days=i)
        strip.append({"date": d, "weekday": WEEKDAYS[d.weekday()], "has_payments": d in pay_days, "iso": d.isoformat()})

    selected_day = None
    raw_day = request.GET.get("day", "")
    try:
        selected_day = datetime.date.fromisoformat(raw_day) if raw_day else None
    except ValueError:
        selected_day = None

    if selected_day:
        upcoming = [s for s in active if s.next_payment_date == selected_day]
    else:
        horizon = today + datetime.timedelta(days=30)
        upcoming = [s for s in active if s.next_payment_date <= horizon]
    upcoming.sort(key=lambda s: s.next_payment_date)
    upcoming_total = sum((s.price for s in upcoming), Decimal("0"))

    tab = "upcoming" if request.GET.get("tab") == "upcoming" or selected_day else "all"
    context = {
        "tab": tab,
        "ring": ring,
        "month_total": month_total,
        "year_total": year_total,
        "active_count": len(active),
        "priciest": priciest,
        "cheapest": cheapest,
        "strip": strip,
        "selected_day": selected_day,
        "upcoming": upcoming,
        "upcoming_total": upcoming_total,
        "subs": subs,
        "today": today,
    }
    return render(request, "subscriptions/dashboard.html", context)


class SubscriptionListView(LoginRequiredMixin, QuerystringMixin, ListView):

    model = Subscription
    template_name = "subscriptions/subscription_list.html"
    context_object_name = "subs"
    paginate_by = 10

    def get_filter_form(self):
        if not hasattr(self, "filter_form"):
            self.filter_form = SubscriptionFilterForm(self.request.GET or None, user=self.request.user)
        return self.filter_form

    def get_queryset(self):
        subs = _user_subs(self.request.user)
        form = self.get_filter_form()
        if form.is_valid():
            data = form.cleaned_data
            if data["q"]:
                subs = subs.filter(Q(name__icontains=data["q"]) | Q(notes__icontains=data["q"]))
            if data["category"]:
                subs = subs.filter(category=data["category"])
            if data["status"]:
                subs = subs.filter(status=data["status"])
            if data["cycle"]:
                subs = subs.filter(billing_cycle=data["cycle"])
            order = {
                "name": ["name"],
                "price_desc": ["-price"],
                "price_asc": ["price"],
            }.get(data["sort"], ["next_payment_date", "name"])
            subs = subs.order_by(*order)
        return subs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active = [s for s in self.object_list if s.is_active]
        context["form"] = self.get_filter_form()
        context["month_total"] = sum((s.monthly_cost for s in active), Decimal("0"))
        context["year_total"] = sum((s.yearly_cost for s in active), Decimal("0"))
        return context


class SubscriptionDetailView(LoginRequiredMixin, DetailView):
    template_name = "subscriptions/subscription_detail.html"

    def get_queryset(self):
        return _user_subs(self.request.user).prefetch_related("tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payments"] = self.object.payments.all()[:10]
        return context


class SubscriptionCreateView(LoginRequiredMixin, CreateView):

    model = Subscription
    form_class = SubscriptionForm
    template_name = "subscriptions/subscription_form.html"
    success_url = reverse_lazy("subscriptions:list")

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        slug = request.GET.get("service", "")
        self.service = get_service(slug)
        self.custom = slug == "custom"

    def get(self, request, *args, **kwargs):
        if not self.service and not self.custom:
            return catalog(request)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.service and not self.custom:
            return catalog(request)
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["service"] = self.service
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"service": self.service, "custom": self.custom, "title": "Нова підписка", "sub": None})
        return context

    def form_valid(self, form):
        sub = form.save(commit=False)
        sub.user = self.request.user
        sub.service = self.service["slug"] if self.service else ""
        sub.save()
        form.save_m2m()
        self.object = sub
        messages.success(self.request, f"Підписку «{sub.name}» додано")
        return HttpResponseRedirect(self.get_success_url())


def catalog(request):
    q = request.GET.get("q", "").strip().lower()
    category = request.GET.get("category", "")
    items = [
        s for s in SERVICES
        if (not q or q in s["name"].lower()) and (not category or s["category"] == category)
    ]
    context = {"items": items, "q": q, "category": category, "categories": catalog_categories()}
    return render(request, "subscriptions/catalog.html", context)


class SubscriptionUpdateView(LoginRequiredMixin, UpdateView):
    form_class = SubscriptionForm
    template_name = "subscriptions/subscription_form.html"
    success_url = reverse_lazy("subscriptions:list")

    def get_queryset(self):
        return _user_subs(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": "Редагування", "sub": self.object, "service": None, "custom": False})
        return context

    def form_valid(self, form):
        messages.success(self.request, "Зміни збережено")
        return super().form_valid(form)


class SubscriptionDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "subscriptions/confirm_delete.html"
    success_url = reverse_lazy("subscriptions:list")
    extra_context = {"kind": "підписку", "cancel_url": reverse_lazy("subscriptions:list")}

    def get_queryset(self):
        return _user_subs(self.request.user)

    def form_valid(self, form):
        sub = self.object
        name = sub.name
        if sub.icon:
            sub.icon.delete(save=False)
        messages.success(self.request, f"Підписку «{name}» видалено")
        return super().form_valid(form)


@login_required
@require_POST
def subscription_paid(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if not sub.is_active:
        messages.error(request, "Оплату можна позначити тільки для активної підписки")
    else:
        sub.mark_paid()
        messages.success(request, f"Оплату «{sub.name}» враховано. Наступний платіж: {sub.next_payment_date:%d.%m.%Y}")
    next_url = request.POST.get("next", "")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("subscriptions:list")


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "subscriptions/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        user = self.request.user
        return _visible_categories(user).annotate(
            sub_count=Count("subscription", filter=Q(subscription__user=user))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CategoryForm(user=self.request.user)
        return context


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "subscriptions/category_detail.html"

    def get_queryset(self):
        return _visible_categories(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subs"] = _user_subs(self.request.user).filter(category=self.object)
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = "subscriptions/category_form.html"
    success_url = reverse_lazy("subscriptions:categories")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        category = form.save(commit=False)
        category.user = self.request.user
        category.save()
        self.object = category
        messages.success(self.request, f"Категорію «{category.name}» додано")
        return HttpResponseRedirect(self.get_success_url())


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "subscriptions/confirm_delete.html"
    success_url = reverse_lazy("subscriptions:categories")
    extra_context = {"kind": "категорію", "cancel_url": reverse_lazy("subscriptions:categories")}

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Категорію видалено")
        return super().form_valid(form)


class TagListView(LoginRequiredMixin, ListView):
    template_name = "subscriptions/tag_list.html"
    context_object_name = "tags"

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).annotate(sub_count=Count("subscriptions"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TagForm(user=self.request.user)
        return context


class TagDetailView(LoginRequiredMixin, DetailView):
    template_name = "subscriptions/tag_detail.html"

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subs"] = _user_subs(self.request.user).filter(tags=self.object)
        return context


class TagCreateView(LoginRequiredMixin, CreateView):
    form_class = TagForm
    template_name = "subscriptions/tag_form.html"
    success_url = reverse_lazy("subscriptions:tags")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        tag = form.save(commit=False)
        tag.user = self.request.user
        tag.save()
        self.object = tag
        messages.success(self.request, f"Тег «{tag.name}» додано")
        return HttpResponseRedirect(self.get_success_url())


class TagDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "subscriptions/confirm_delete.html"
    success_url = reverse_lazy("subscriptions:tags")
    extra_context = {"kind": "тег", "cancel_url": reverse_lazy("subscriptions:tags")}

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Тег видалено")
        return super().form_valid(form)


class PaymentListView(LoginRequiredMixin, QuerystringMixin, ListView):
    template_name = "subscriptions/payment_list.html"
    context_object_name = "payments"
    paginate_by = 10

    def get_queryset(self):
        return Payment.objects.filter(subscription__user=self.request.user).select_related("subscription")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = self.object_list.aggregate(total=Sum("amount"))["total"]
        return context


class PaymentDetailView(LoginRequiredMixin, DetailView):
    template_name = "subscriptions/payment_detail.html"

    def get_queryset(self):
        return Payment.objects.filter(subscription__user=self.request.user).select_related("subscription")


class ManagerOverviewView(PermissionRequiredMixin, TemplateView):

    permission_required = "subscriptions.view_all_stats"
    template_name = "subscriptions/manager_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active = Q(subscription__status=Subscription.Status.ACTIVE)
        context["rows"] = User.objects.annotate(
            sub_count=Count("subscription", filter=active),
            total=Sum("subscription__price", filter=active),
        ).order_by("-total", "username")
        context["summary"] = Subscription.objects.filter(status=Subscription.Status.ACTIVE).aggregate(
            count=Count("id"), total=Sum("price"), average=Avg("price")
        )
        context["payments_count"] = Payment.objects.count()
        return context
