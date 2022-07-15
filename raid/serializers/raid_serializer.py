from rest_framework import serializers


class BossRaidRakingSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    account = serializers.CharField()
    nickname = serializers.CharField()
    total_score = serializers.IntegerField()


class BossRaidHistorySerializer(serializers.Serializer):
    top_ranker_info_list = BossRaidRakingSerializer(many=True)
    my_ranking = BossRaidRakingSerializer()
