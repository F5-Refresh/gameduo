from raid import models
from rest_framework import serializers


class BossRaidRakingSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    nickname = serializers.CharField()
    total_score = serializers.IntegerField()


class BossRaidHistorySerializer(serializers.Serializer):
    top_ranker_info_list = BossRaidRakingSerializer(many=True)
    my_ranking = BossRaidRakingSerializer()
