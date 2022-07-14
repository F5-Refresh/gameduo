import jwt
from django.core.cache import cache
from django.db import connection
from django.db.models import F, Sum
from django.db.models.expressions import Window
from django.db.models.functions import Rank
from drf_yasg.utils import swagger_auto_schema
from gameduo.settings import SECRET_KEY
from raid.models import RaidHistory
from raid.serializers.raid_serializer import BossRaidHistorySerializer, BossRaidRakingSerializer
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, status


class BossRaidRankingView(APIView):
    """raid ranking 조회 view

    Writer: 조병민
    Date: 2022-07-11

    GET: 레이드의 ranking Top10과 현재 유저의 랭킹을 조회

    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ranking get func

        access token에서 user id를 추출, 해당 id로 top100과 자기자신의 ranking을 반환
        """

        cache_data = cache.get('ranking')
        if not cache_data:
            try:
                """Top100 ranking data"""
                ranking_data = (
                    RaidHistory.objects.values('user')
                    .annotate(total_score=Sum('score'), nickname=F('user__nickname'))
                    .annotate(rank=Window(expression=Rank(), order_by=F('total_score').desc()))
                )[:100]

                # header추출
                # access_token = request.META['HTTP_AUTHORIZATION']
                # de_token = jwt.decode(access_token, SECRET_KEY, 'HS256')

                access_token = request.META['HTTP_AUTHORIZATION']
                decoded = jwt.decode(access_token, SECRET_KEY, 'HS256')
                """my ranking data

                subquery를 사용하여 data searching이 필요하다고 판단
                ORM만으로는 subquery의 한계가 있다고 생각하여 
                row query로 작성
                """
                query_string = f"""
                        WITH ranking(user_id, total_score, `rank` ) AS (
	                        SELECT
		                        user_id,
		                        SUM(rh.score) as total_score,
		                        RANK() OVER (ORDER BY SUM(rh.score) DESC) AS `rank`
	                        FROM raid_history rh
                            GROUP BY rh.user_id
                        )
                        SELECT 
                                us.id, 
                                us.nickname,
                                rk.`rank`,
                                rk.total_score
                        FROM `user` us
	                        JOIN ranking rk ON us.id = rk.user_id
                            WHERE us.id = '{decoded['user_id']}'
                    """

                with connection.cursor() as c:
                    c.execute(query_string)
                    # execute의 반환 type은 tuple 이기때문에 description에서 column 명을 추출 후 zip을 해주지 않으면 serializer에 적용을 시킬 수 가 없다
                    columns = [col[0] for col in c.description]
                    my_ranking = dict(zip(columns, c.fetchone()))

                my_ranking = BossRaidRakingSerializer(my_ranking)
                total_ranking_serialize = BossRaidRakingSerializer(ranking_data, many=True)
                cache_data = {
                    'top_ranker_info_list': total_ranking_serialize.data,
                    'my_ranking': my_ranking.data,
                }

                ranking_info = BossRaidHistorySerializer(cache_data)

                cache_data = ranking_info.data
                cache.set('ranking', cache_data, 300)
            except Exception as ex:
                raise APIException(detail='error occurred', code=ex)

        return Response(cache_data, status=status.HTTP_200_OK)
