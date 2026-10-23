from decimal import Decimal

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static

from subscriptions.catalog import find_by_name, get_service

register = template.Library()

def _normalize(name):
    return "".join(ch for ch in name.lower() if ch.isalnum())


def _service(name, slug=""):
    
    return get_service(slug) or find_by_name(name)



ICON_EXTS = ("png", "webp", "jpg", "jpeg", "svg")
_icon_cache = {}


def _icon_path(icon):
    
    if not settings.DEBUG and icon in _icon_cache:
        return _icon_cache[icon]
    found = None
    for ext in ICON_EXTS:
        rel = f"subscriptions/icons/{icon}.{ext}"
        if finders.find(rel):
            found = rel
            break
    _icon_cache[icon] = found
    return found


def _hue(name):
    return sum(ord(ch) for ch in _normalize(name)) * 37 % 360


@register.filter
def uah(value):
    
    if value is None or value == "":
        return ""
    value = Decimal(value)
    return f"{value:,.2f}".replace(",", " ") + " ₴"


@register.filter
def uah_short(value):
    
    if value is None or value == "":
        return ""
    value = Decimal(value)
    if value == value.to_integral_value():
        return f"{value:,.0f}".replace(",", " ") + " ₴"
    return uah(value)


FAVICON = "https://www.google.com/s2/favicons?domain={domain}&sz=128"


@register.inclusion_tag("partials/service_icon.html")
def service_icon(name, size=40, service="", icon=None):
    
    src = remote = None
    if icon:
        src = icon.url
    else:
        found = _service(name, service)
        path = _icon_path(found["icon"]) if found else None
        if path:
            src = static(path)
        elif found and found.get("domain"):
            remote = FAVICON.format(domain=found["domain"])
    return {
        "src": src,
        "remote": remote,
        "letter": name.strip()[:1].upper() or "?",
        "hue": _hue(name),
        "size": size,
    }


@register.simple_tag
def brand_color(name, service=""):
    
    found = _service(name, service)
    return found["color"] if found else f"hsl({_hue(name)} 55% 50%)"
