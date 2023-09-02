from django.db import models

# models.py

class GameData(models.Model):
    team_id = models.IntegerField()
    date = models.DateField()
    game_data = models.JSONField()
    fetched_at = models.DateTimeField(auto_now=True)
