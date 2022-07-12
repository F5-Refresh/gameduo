from raid import models
from rest_framework import serializers


class BossRaidRakingSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    total_score = serializers.IntegerField()


class BossRaidHistorySerializer(serializers.ModelSerializer):
    top_ranker_info_list = BossRaidRakingSerializer(many=True)
    my_ranking = BossRaidRakingSerializer()

    class Meta:
        model = models.RaidHistory
        fields = '__all__'
