from django.core.cache import cache
from django.shortcuts import get_object_or_404
from raid.models import RaidHistory
from rest_framework import serializers


class BossRaidHistorySerializer(serializers.ModelSerializer):
    def create(self, data):
        user, level = data.get('user'), data.get('level')
        return RaidHistory.objects.create(user=user, level=level)

    def validate_level(self, level):
        if cache.get(f"level{level}") == None:
            raise serializers.ValidationError({'detail': '유효한 레벨이 아닙니다.'})
        return level

    class Meta:
        model = RaidHistory
        fields = ['user', 'level']
