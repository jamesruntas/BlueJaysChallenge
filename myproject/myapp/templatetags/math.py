from django import template

register = template.Library()

@register.filter
def win_percentage(w, l):
    if w + l == 0:
        return 0
    return round((w / (w + l)) * 1000)


@register.filter
def url_player_id_headshot(id):
    template = "https://img.mlbstatic.com/mlb-photos/image/upload/w_60,d_people:generic:headshot:silo:current.png,q_auto:best,f_auto/v1/people/{}/headshot/silo/current"
    headShotUrl = template.format(id)
    return headShotUrl 

