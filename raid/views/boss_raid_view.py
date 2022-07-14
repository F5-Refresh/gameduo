import threading
import time
from email import message

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from raid.models import RaidHistory
from raid.serializers.boss_raid_serializer import BossRaidHistorySerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class BossRaidView(APIView):

    """보스레이드 API 뷰
    Writer: 이동연
    Date: 2022-07-14

    보스 레이드 시작: [POST] /raid/start_raid
    보스 레이드 종료: [POST] /raid/end_raid
    """

    permission_classes = [IsAuthenticated]

    @api_view(['POST'])
    def start_boss_raid(request):

        """
        보스레이드의 참여에 대한 액션입니다.
        """

        if not cache.get('can_enter'):  # 레이드는 한 유저씩만 입장가능합니다. 동시성을 고려했습니다.
            return Response({'message': '다른유저가 이미 레이드에 입장해있습니다.', 'is_entered': False}, status=status.HTTP_200_OK)

        user = request.user
        level = request.data.get('level')
        boss_raid_history = BossRaidHistorySerializer(data={'user': user.id, 'level': level})

        if boss_raid_history.is_valid():
            boss_raid_history = boss_raid_history.save()
            setting_raid_status(False, user.id)
            timemer = threading.Thread(target=game_timmer(boss_raid_history))  # 제한시간 후 자동 패배의 액션입니다.
            timemer.setDaemon(True)
            timemer.start()
            return Response({'message': '유저가 레이드에 입장했습니다', 'is_entered': True}, status=status.HTTP_200_OK)
        else:
            return Response(boss_raid_history.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    def end_boss_raid(request):

        """
        보스레이드의 종료에 대한 액션입니다.
        """

        boss_raid_history = get_object_or_404(RaidHistory, user=request.user.id, end_time=None)

        if bool(request.data.get('is_win')):
            if (score := cache.get(f'level{boss_raid_history.level}')) == None:
                return Response({'detail': '레벨이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
            boss_raid_history.score = score

        setting_raid_status(can_enter=True)
        boss_raid_history.game_over()

        return Response(
            {'message': '레이드가 정상적으로 종료 되었습니다.', 'boss_raid_history_id': boss_raid_history.id},
            status=status.HTTP_200_OK,
        )


def game_timmer(boss_raid_history):
    time.sleep(cache.get('limit_time'))
    if not cache.get('can_enter'):  # 제한시간이 지나도 레이드가 끝나지 않을경우 자동으로 패배처리를 합니다.
        setting_raid_status(can_enter=True)
        boss_raid_history.game_over()


def setting_raid_status(can_enter, user_id=None):
    cache.set('can_enter', can_enter)
    cache.set('entered_user_id', user_id)
