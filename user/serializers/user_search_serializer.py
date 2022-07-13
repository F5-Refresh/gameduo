from raid.models import RaidHistory
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class UserSearchSerializer(ModelSerializer):
    """유저정보 조회 시리얼라이저

    Writer: 김동규
    Date: 2022-07-12
    """

    enter_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    def get_enter_time(self, obj):
        return (obj.enter_time).strftime('%Y-%m-%d %H:%M')

    def get_end_time(self, obj):
        if obj.end_time:
            return (obj.end_time).strftime('%Y-%m-%d %H:%M')
        return None

    class Meta:
        model = RaidHistory
        fields = ['id', 'score', 'enter_time', 'end_time']


class UserSearchSchema(serializers.Serializer):
    """유저정보 조회 Schema 시리얼라이저

    Writer: 김동규
    Date: 2022-07-12

    해당 시리얼라이저는 오직 Swagger Schema를 위해 사용됩니다.
    """

    nickname = serializers.CharField(max_length=100)
    total_score = serializers.IntegerField()
    boss_raid_histories = UserSearchSerializer(many=True)
