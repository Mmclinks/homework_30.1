import re
from django.core.exceptions import ValidationError

def validate_youtube_link(value):
    # Проверяем, что ссылка на YouTube
    youtube_regex = r"^(https?://)?(www\.)?youtube\.com/.+"
    if value and not re.match(youtube_regex, value):
        raise ValidationError("Ссылки на сторонние ресурсы, кроме youtube.com, не допускаются.")
