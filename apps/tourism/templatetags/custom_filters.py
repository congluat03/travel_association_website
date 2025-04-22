# apps/tourism/templatetags/custom_filters.py

import os
from django import template
from django.conf import settings

register = template.Library()

@register.filter
def files_in_dir(folder_path):
    abs_path = os.path.join(settings.BASE_DIR, folder_path)
    if os.path.isdir(abs_path):
        return [
            f for f in os.listdir(abs_path)
            if os.path.isfile(os.path.join(abs_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
        ]
    return []
