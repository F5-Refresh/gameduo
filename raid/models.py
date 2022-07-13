from datetime import datetime

from core.models import TimeStampModel
from django.db import models


class RaidHistory(TimeStampModel):
    user = models.ForeignKey('user.User', related_name='raid_histories', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    enter_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    level = models.PositiveIntegerField()
    delete_flag = models.BooleanField(default=False)

    class Meta:
        db_table = 'raid_history'

    def game_over(self):
        self.end_time = datetime.now()
        self.save()
