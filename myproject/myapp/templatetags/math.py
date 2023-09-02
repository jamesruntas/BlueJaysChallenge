from django import template

register = template.Library()

@register.filter
def win_percentage(w, l):
    if w + l == 0:
        return 0
    return round((w / (w + l)) * 1000)
