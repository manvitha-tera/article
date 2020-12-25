from urllib.parse import urlparse

from  django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def get_url_hostname(url):
    try:
        validate = URLValidator(
            schemes=("http", "https", "ftp", "ftps", "rtsp", "rtmp")
        )
        validate(url)
    except (ValueError, ValidationError):
        return None

    parsed = urlparse(url)
    return parsed.hostname





