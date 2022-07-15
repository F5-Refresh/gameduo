from base64 import b64decode
from os import readlink

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
        """get Top ranking And My ranking API

        access token에서 user id를 추출, 해당 id로 top100과 자기자신의 ranking을 반환
        """

        try:
            top_ranking_cache_data = cache.get('top_ranking_list')
            if not top_ranking_cache_data:

                # Top100 ranking data
                ranking_data = (
                    RaidHistory.objects.values('user')
                    .annotate(total_score=Sum('score'), nickname=F('user__nickname'), account=F('user__account'))
                    .annotate(rank=Window(expression=Rank(), order_by=F('total_score').desc()))
                )[:10]

                # MySql의 RANK함수는 1부터 시작하지만 요구사항에 따라 0부터 시작되어야하기때문에
                for ranker in ranking_data:
                    ranker['rank'] = ranker['rank'] - 1

                total_ranking_serialize = BossRaidRakingSerializer(ranking_data, many=True).data
                top_ranking_cache_data = total_ranking_serialize
                cache.set('top_ranking_list', top_ranking_cache_data, 120)

            # header추출
            # simple_JWT에서 request에 인증된 유저 정보를 담아 주지만 decode를 사용해보고 싶었음.
            access_token = (
                request.META['HTTP_AUTHORIZATION'].split(' ')[1]
                if len(request.META['HTTP_AUTHORIZATION'].split(' ')) != 1
                else request.META['HTTP_AUTHORIZATION']
            )
            decoded = jwt.decode(access_token, SECRET_KEY, 'HS256')
            print(decoded)
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
                                us.account,
                                us.nickname,
                                rk.`rank` ,
                                rk.total_score
                        FROM `user` us
	                        LEFT JOIN ranking rk ON us.id = rk.user_id
                            WHERE us.id = '{decoded['user_id'].replace('-','')}'
                    """
            with connection.cursor() as c:
                c.execute(query_string)
                # execute의 반환 type은 tuple 이기때문에 description에서 column 명을 추출 후 zip을 해주지 않으면 serializer에 적용을 시킬 수 가 없다
                columns = [col[0] for col in c.description]
                my_ranking = dict(zip(columns, c.fetchone()))

            my_ranking['rank'] = my_ranking['rank'] - 1 if type(my_ranking['rank']) == int else None

            my_ranking = BossRaidRakingSerializer(my_ranking).data

            ranking_info = {
                'top_ranker_info_list': top_ranking_cache_data,
                'my_ranking': my_ranking,
            }

        except Exception as ex:
            print(ex)
            raise APIException(detail='error occurred', code=ex)

        return Response({'ranking_info': ranking_info}, status=status.HTTP_200_OK)
