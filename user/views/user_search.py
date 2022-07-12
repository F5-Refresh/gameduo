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
    permission_classes = [IsAuthenticated]

    user_id = openapi.Parameter('user_id', openapi.IN_PATH, required=True, type=openapi.TYPE_STRING)

    @swagger_auto_schema(responses={200: UserSearchSchema}, manual_parameters=[user_id])
    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({'detail': f'{user_id} 유저는 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        raid_histories = RaidHistory.objects.filter(user=user)

        data = {
            'nickname': user.nickname,
            'total_score': sum([data.score for data in raid_histories]),
            'boss_raid_histories': UserSearchSerializer(raid_histories, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)
