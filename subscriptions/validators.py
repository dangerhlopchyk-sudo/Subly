import datetime

from django.core.exceptions import ValidationError


def validate_reasonable_date(value):
    today = datetime.date.today()
    if value < datetime.date(2000, 1, 1):
        raise ValidationError("Дата не може бути раніше 2000 року", code="too_old")
    if value > today.replace(year=today.year + 10):
        raise ValidationError("Дата не може бути далі ніж через 10 років", code="too_far")


def validate_not_blank(value):
    if not value.strip():
        raise ValidationError("Поле не може бути порожнім", code="blank")


ICON_MAX_BYTES = 5 * 1024 * 1024
_SIGNATURES = {
    "png": (b"\x89PNG\r\n\x1a\n",),
    "jpg": (b"\xff\xd8\xff",),
    "jpeg": (b"\xff\xd8\xff",),
    "gif": (b"GIF87a", b"GIF89a"),
    "webp": (b"RIFF",),
}


def validate_icon(file):
    ext = file.name.rsplit(".", 1)[-1].lower() if "." in file.name else ""
    if ext not in _SIGNATURES:
        raise ValidationError("Підтримуються лише файли PNG, JPG, WEBP або GIF")
    if file.size > ICON_MAX_BYTES:
        raise ValidationError("Файл завеликий: максимум 5 МБ")
    head = file.read(12)
    file.seek(0)
    if not any(head.startswith(sig) for sig in _SIGNATURES[ext]) or (ext == "webp" and head[8:12] != b"WEBP"):
        raise ValidationError("Файл не схожий на зображення")
