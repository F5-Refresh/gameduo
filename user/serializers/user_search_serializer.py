from raid.models import RaidHistory
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer


class UserSearchSerializer(ModelSerializer):
    enter_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    def get_enter_time(self, obj):
        return (obj.enter_time).strftime("%Y-%m-%d %H")

    def get_end_time(self, obj):
        if obj.end_time:
            return (obj.end_time).strftime("%Y-%m-%d %H")
        return None

    class Meta:
        model = RaidHistory
        fields = ['id', 'score', 'enter_time', 'end_time']


# only for swagger
class UserSearchSchema(Serializer):
    nickname = serializers.CharField(max_length=100)
    total_score = serializers.IntegerField()
    boss_raid_histories = UserSearchSerializer(many=True)
