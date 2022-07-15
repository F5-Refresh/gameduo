from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from raid.models import RaidHistory
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializers.user_search_serializer import UserSearchSchema, UserSearchSerializer


class UserSearchView(APIView):
    """유저정보 조회 기능 API

    Writer: 김동규
    Date: 2022-07-12

    특정 유저의 보스레이드 히스토리를 조회합니다.
    """

    permission_classes = [IsAuthenticated]

    offset = openapi.Parameter(
        'offset', openapi.IN_QUERY, required=False, pattern='?offset=', type=openapi.TYPE_STRING
    )
    limit = openapi.Parameter('limit', openapi.IN_QUERY, required=False, pattern='?limit=', type=openapi.TYPE_STRING)
    account = openapi.Parameter('account', openapi.IN_PATH, required=True, type=openapi.TYPE_STRING)

    @swagger_auto_schema(responses={200: UserSearchSchema}, manual_parameters=[account, offset, limit])
    def get(self, request, account):
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))

        user = get_object_or_404(User, account=account)
        raid_histories = RaidHistory.objects.filter(user=user).order_by('-enter_time')[offset : offset + limit]

        data = {
            'nickname': user.nickname,
            'total_score': sum([data.score for data in raid_histories]),
            'boss_raid_histories': UserSearchSerializer(raid_histories, many=True).data,
        }

        return Response(data, status=status.HTTP_200_OK)
