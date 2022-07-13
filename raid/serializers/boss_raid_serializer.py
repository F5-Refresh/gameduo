from django.shortcuts import get_object_or_404
from raid.models import RaidHistory
from rest_framework import serializers


class BossRaidHistorySerializer(serializers.ModelSerializer):
    def create(self, data):
        user, level = data.get('user'), data.get('level')
        return RaidHistory.objects.create(user=user, level=level)

    class Meta:
        model = RaidHistory
        fields = ['user', 'level']
