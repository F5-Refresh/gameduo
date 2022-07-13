from django.core.cache import cache
from django.db.models import F, FilteredRelation, OuterRef, Q, Subquery, Sum
from django.db.models.expressions import Window
from django.db.models.functions import Rank
from drf_yasg.utils import swagger_auto_schema
from raid.models import RaidHistory
from raid.serializers.raid_serializer import BossRaidRakingSerializer
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView, status
from user.models import User


class BossRaidRankingView(APIView):
    '''raid ranking 조회 view

    Writer: 조병민
    Date: 2022-07-11

    GET: 레이드의 ranking Top10과 현재 유저의 랭킹을 조회

    '''

    # TODO: Django ORM의 Subquery문제로 my-ranking 구현 x
    # TODO: 멘토님꼐 질문 남겨놓음
    def get(self, request):

        cache_data = cache.get('ranking')
        if not cache_data:
            try:

                ranking_data = (
                    RaidHistory.objects.values('user')
                    .annotate(total_score=Sum('score'), nickname=F('user__nickname'))
                    .annotate(rank=Window(expression=Rank(), order_by=F('total_score').desc()))
                )[:100]

                # my_ranking = (
                #     RaidHistory.objects.values('user')
                #     .annotate(total_score=Sum('score'), nickname=F('user__nickname'))
                #     .annotate(rank=Window(expression=Rank(), order_by=F('total_score').desc()))
                # )

                total_ranking_serialize = BossRaidRakingSerializer(ranking_data, many=True)
                # my_ranking_serialize = BossRaidRakingSerializer(my_ranking, many=True)
                # cache_data = {
                #     'top_ranker_info_list': total_ranking_serialize.data,
                #     'my_ranking': my_ranking_serialize.data,
                # }
                cache_data = total_ranking_serialize.data
                cache.set('ranking', cache_data, 360)
            except Exception as ex:
                print(ex)
                raise APIException(detail='error occurred', code=ex)

        return Response(cache_data, status=status.HTTP_200_OK)
