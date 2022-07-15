from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from raid.serializers.raid_status_serach_serializers import RaidStatusSearchSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class RaidStatusSearchView(APIView):
    """보스레이드 상태조회 기능 API

    Writer: 김동규
    Date: 2022-07-14

    현재 보스레이드에 입장할 수 있는 상태인지를 확인합니다.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: RaidStatusSearchSerializer})
    def get(self, request):
        can_enter = cache.get('can_enter')
        entered_user_id = cache.get('entered_user_id')

        data = {'can_enter': can_enter, 'entered_user_id': entered_user_id}

        serializer = RaidStatusSearchSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
