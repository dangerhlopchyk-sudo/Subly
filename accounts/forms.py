from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.render_value = True

    @property
    def credentials_invalid(self):
        return self.is_bound and bool(self.non_field_errors())


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Електронна пошта")

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {"username": "Ім'я користувача"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("password1", "password2"):
            self.fields[name].widget.render_value = True
        self.fields["password1"].help_text = ""

    def password_rules(self):
        password = self.data.get("password1", "") if self.is_bound else ""
        candidate = User(username=self.data.get("username", ""), email=self.data.get("email", ""))
        rules = []
        for validator in password_validation.get_default_password_validators():
            ok = None
            if password:
                try:
                    validator.validate(password, candidate)
                    ok = True
                except ValidationError:
                    ok = False
            rules.append({"text": validator.get_help_text(), "ok": ok, "bad": ok is False})
        return rules

    @property
    def password_invalid(self):
        if not self.is_bound:
            return False
        return bool(self.errors.get("password1")) or any(r["bad"] for r in self.password_rules())

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Користувач з такою поштою вже існує")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user