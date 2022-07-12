from django.core.cache import cache
from django.db.models import F, Sum
from drf_yasg.utils import swagger_auto_schema
from raid.models import RaidHistory
from raid.serializers.raid_serializer import BossRaidRakingSerializer
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView, status


class BossRaidRankingView(APIView):
    '''raid ranking 조회 view

    Writer: 조병민
    Date: 2022-07-11

    GET: 레이드의 ranking Top10과 현재 유저의 랭킹을 조회

    '''

    # TODO: mysql 5.7에서 rank와 rownum을 지원을 하지 않음. top10만 뽑는건 큰 문제가 되지 않으나
    # TODO: myranking에서의 rank를 어떻게 나타 낼지 고민 해봐야됨
    def get(self, request):

        cache_data = cache.get('ranking')
        print(cache_data)
        if not cache_data:
            try:
                ranking_data = (
                    RaidHistory.objects.values('user')
                    .annotate(total_score=Sum('score'), user_id=F('user__user_id'))
                    .order_by('-total_score')
                )

                my_ranking = (
                    RaidHistory.objects.filter(user__id='43aa2e78-6a9f-4a15-91d8-ee5011f3')
                    .values('user')
                    .annotate(total_score=Sum('score'))
                )

                for i in range(len(ranking_data)):
                    ranking_data[i]['ranking'] = i + 1

                top_ranking_serialize = BossRaidRakingSerializer(ranking_data, many=True)

                cache.set('ranking', top_ranking_serialize.data, 360)
                cache_data = top_ranking_serialize.data
            except Exception as ex:
                print(ex)
                raise APIException(detail='error occurred', code=ex)

        return Response(data={"ranking": cache_data}, status=status.HTTP_200_OK)
