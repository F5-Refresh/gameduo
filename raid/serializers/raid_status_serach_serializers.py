from rest_framework import serializers


class RaidStatusSearchSerializer(serializers.Serializer):
    """보스레이드 상태조회 시리얼라이저

    Writer: 김동규
    Date: 2022-07-12

    """

    can_enter = serializers.BooleanField(allow_null=True)
    entered_user_id = serializers.UUIDField(allow_null=True)
