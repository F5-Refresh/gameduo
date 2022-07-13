import threading
import time
from email import message

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from raid.models import RaidHistory
from raid.serializers.boss_raid_serializer import BossRaidHistorySerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class BossRaidView(APIView):
    @api_view(['POST'])
    def start_boss_raid(request):
        print(request)
        if cache.get('is_use'):
            return Response({'message': 'anther user already entered', 'is_entered': False}, status=status.HTTP_200_OK)

        data = {'user': request.user.id, 'level': request.data.get('level')}
        boss_raid_history = BossRaidHistorySerializer(data=data)
        if boss_raid_history.is_valid():  # 레이드 참가에 대한  기록 O
            boss_raid_history = boss_raid_history.save()  # 레코드 만듬
            cache.set('is_use', True)
            timemer = threading.Thread(target=game_timmer(boss_raid_history))
            timemer.setDaemon(True)
            timemer.start()
            return Response({'message': 'user entered', 'is_entered': True}, status=status.HTTP_200_OK)
        else:
            return Response(boss_raid_history.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    def end_boss_raid(request):
        boss_raid_history = get_object_or_404(RaidHistory, user=request.user.id, end_time=None)
        if bool(request.data.get('is_win')):
            if (score := cache.get(f'level{boss_raid_history.level}')) == None:
                return Response({'detail': '레벨이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
            boss_raid_history.score = score
        boss_raid_history.game_over()
        return Response(
            {'message': '레이드가 정상적으로 종료 되었습니다.', 'boss_raid_history_id': boss_raid_history.id},
            status=status.HTTP_200_OK,
        )


def game_timmer(boss_raid_history):
    print('sub thread sleep')
    time.sleep(cache.get('limit_time'))  # 180
    if cache.get('is_use'):
        cache.set('is_use', False)
        boss_raid_history.game_over()
