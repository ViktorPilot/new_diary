from django import template

register = template.Library()


@register.filter()
def media_filter(path: str) -> str:
    """Функция, преобразующая путь к медиафайлам"""
    if path:
        return f"/media/{path}"
    return "#"
