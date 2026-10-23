import datetime

from django import forms
from django.db.models import Q

from .models import Category, Subscription, Tag


class SubscriptionForm(forms.ModelForm):

    def __init__(self, *args, user=None, service=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.service = service
        self.fields["category"].queryset = Category.objects.filter(
            Q(user__isnull=True) | Q(user=user)
        )
        self.fields["category"].empty_label = "Без категорії"
        self.fields["tags"].queryset = Tag.objects.filter(user=user)
        self.fields["tags"].required = False
        self.fields["remove_icon"] = forms.BooleanField(label="Прибрати своє зображення", required=False)
        if service:
            del self.fields["icon"]
            del self.fields["remove_icon"]
            self.fields["name"].required = False
            self.fields["name"].widget = forms.HiddenInput()
            self.initial["name"] = service["name"]
            self.initial.setdefault(
                "category",
                Category.objects.filter(user__isnull=True, name=service["category"]).first(),
            )
            if service["price"]:
                self.fields["price"].widget.attrs["placeholder"] = f"наприклад, {service['price']}"

    class Meta:
        model = Subscription
        fields = [
            "name", "icon", "category", "tags", "price", "billing_cycle",
            "next_payment_date", "status", "auto_renew", "notes",
        ]
        widgets = {
            "next_payment_date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
            "icon": forms.FileInput(attrs={"accept": "image/png,image/jpeg,image/webp,image/gif"}),
            "tags": forms.CheckboxSelectMultiple(),
            "price": forms.NumberInput(attrs={"step": "1", "min": "0"}),
        }
        error_messages = {
            "name": {"required": "Вкажіть назву підписки", "max_length": "Назва задовга: максимум 100 символів"},
            "price": {"required": "Вкажіть вартість", "invalid": "Введіть число, наприклад 199.00"},
            "next_payment_date": {"required": "Вкажіть дату наступного платежу", "invalid": "Невірний формат дати"},
        }

    def clean_name(self):
        if self.service:
            name = self.service["name"]
        else:
            name = " ".join(self.cleaned_data["name"].split())
        duplicates = Subscription.objects.filter(user=self.user, name__iexact=name)
        if self.instance.pk:
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise forms.ValidationError("У вас уже є підписка з такою назвою")
        return name

    def save(self, commit=True):
        old_icon = self.initial.get("icon") if self.instance.pk else None
        sub = super().save(commit=False)
        if self.cleaned_data.get("remove_icon") and not self.files.get("icon"):
            sub.icon = ""
        if old_icon and (self.files.get("icon") or not sub.icon):
            old_icon.storage.delete(old_icon.name)
        if commit:
            sub.save()
            self.save_m2m()
        return sub

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get("next_payment_date")
        status = cleaned.get("status")
        if date and status == Subscription.Status.ACTIVE:
            if date < datetime.date.today() - datetime.timedelta(days=365):
                self.add_error(
                    "next_payment_date",
                    "Для активної підписки дата платежу не може бути старшою за рік",
                )
        return cleaned


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Category
        fields = ["name", "color"]
        widgets = {"color": forms.TextInput(attrs={"type": "color"})}

    def clean_name(self):
        name = " ".join(self.cleaned_data["name"].split())
        exists = Category.objects.filter(
            Q(user__isnull=True) | Q(user=self.user), name__iexact=name
        ).exists()
        if exists:
            raise forms.ValidationError("Така категорія вже є")
        return name


class TagForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Tag
        fields = ["name"]
        error_messages = {
            "name": {"required": "Вкажіть назву тега", "max_length": "Назва задовга: максимум 30 символів"},
        }

    def clean_name(self):
        name = " ".join(self.cleaned_data["name"].split())
        if Tag.objects.filter(user=self.user, name__iexact=name).exists():
            raise forms.ValidationError("Такий тег уже є")
        return name


class SubscriptionFilterForm(forms.Form):

    SORT_CHOICES = [
        ("date", "За датою платежу"),
        ("name", "За назвою"),
        ("price_desc", "Спочатку дорожчі"),
        ("price_asc", "Спочатку дешевші"),
    ]

    q = forms.CharField(label="Пошук", required=False)
    category = forms.ModelChoiceField(
        label="Категорія", queryset=Category.objects.none(), required=False, empty_label="Усі категорії"
    )
    status = forms.ChoiceField(
        label="Статус", required=False, choices=[("", "Усі статуси")] + Subscription.Status.choices
    )
    cycle = forms.ChoiceField(
        label="Період", required=False, choices=[("", "Будь-який період")] + Subscription.Cycle.choices
    )
    sort = forms.ChoiceField(label="Сортування", required=False, choices=SORT_CHOICES)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(Q(user__isnull=True) | Q(user=user))
