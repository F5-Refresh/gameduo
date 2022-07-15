from background_task import background
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from raid.models import RaidHistory
from raid.serializers.raid_serializer import RaidHistorySerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class RaidView(APIView):

    """보스레이드 API 뷰
    Writer: 이동연
    Date: 2022-07-14

    보스 레이드 시작: [POST] /raid/start_raid
    보스 레이드 종료: [POST] /raid/end_raid
    """

    permission_classes = [IsAuthenticated]

    @api_view(['POST'])
    def start_raid(request):

        """
        보스레이드의 참여에 대한 액션입니다.
        """

        if not cache.get('can_enter'):  # 레이드는 한 유저씩만 입장가능합니다. 동시성을 고려했습니다.
            return Response({'message': '다른유저가 이미 레이드에 입장해있습니다.', 'is_entered': False}, status=status.HTTP_200_OK)

        user = request.user
        level = request.data.get('level')
        raid_history = RaidHistorySerializer(data={'user': user.id, 'level': level})

        if raid_history.is_valid():
            raid_history = raid_history.save()
            setting_raid_status(False, user.id)
            game_timmer(raid_history.id)  # 제한시간이 지나면 자동으로 전투가 종료되는 스케줄링 입니다.
            return Response({'message': '유저가 레이드에 입장했습니다', 'is_entered': True}, status=status.HTTP_200_OK)
        else:
            return Response(raid_history.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    def end_raid(request):

        """
        보스레이드의 종료에 대한 액션입니다.
        """
        raid_history = get_object_or_404(RaidHistory, user=request.user.id, end_time=None)

        if bool(request.data.get('is_win') == 'true'):
            if (score := cache.get(f'level{raid_history.level}')) == None:
                return Response({'detail': '레벨이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
            raid_history.score = score
        setting_raid_status(can_enter=True)
        raid_history.game_over()

        return Response(
            {'message': '레이드가 정상적으로 종료 되었습니다.', 'raid_history_id': raid_history.id},
            status=status.HTTP_200_OK,
        )


@background(schedule=cache.get('limit_time'))
def game_timmer(raid_history_id):
    raid_history = RaidHistory.objects.get(id=raid_history_id)
    print(f"{raid_history.user.nickname}님의 레이드가 자동 종료되었습니다.")
    if not cache.get('can_enter'):  # 제한시간이 지나도 레이드가 끝나지 않을경우 자동으로 패배처리를 합니다.
        setting_raid_status(can_enter=True)
        raid_history.game_over()


def setting_raid_status(can_enter, user_id=None):
    cache.set('can_enter', can_enter)
    cache.set('entered_user_id', user_id)
