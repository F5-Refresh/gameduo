import json
import random
from datetime import datetime, timedelta

from raid.models import RaidHistory
from rest_framework.test import APITestCase
from rest_framework.views import status
from user.models import User


class RaidRankingSearchTest(APITestCase):
    """레이드 랭킹 조회 Test

    Writer: 조병민
    Date: 2022-07-14

    Top100 랭킹 목록과 로그인 된 유저의 현재 랭킹을 반화하는 API를 테스트
    """

    def setUp(self):
        self.url = '/raid/ranking'
        self.users = [
            User.objects.create_user(account='test-user1', nickname='user1', password='testPassword1!'),
            User.objects.create_user(account='test-user2', nickname='user2', password='testPassword1!'),
            User.objects.create_user(account='test-user3', nickname='user3', password='testPassword1!'),
        ]
        self.total_score = dict()
        level_score = [(1, 10), (2, 20), (3, 30)]

        for i in range(12):
            rand1 = random.randint(0, 2)
            rand2 = random.randint(0, 2)
            RaidHistory.objects.create(
                id=i + 1,
                level=level_score[rand1][0],
                score=level_score[rand1][1],
                user=self.users[rand2],
                end_time=(datetime.now() + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M'),
            )

        print('complete set up')

    def return_access_token(self, account: str, password: str) -> str:
        data = {'account': 'test-user1', 'password': 'testPassword1!'}
        response = self.client.post('/users/login/', data)
        return response.data['access_token']

    def test_sucess_searching_ranking_with_access_token(self):
        """
        token decode하여 유저 id를 추출하고 top랭킹과 유저 ranking을 반환 (200)
        """

        access_token = self.return_access_token('test-user1', 'testPassword1!')

        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        response = self.client.get(self.url, content_type='application/json', **headers)

        """
        ranking data는 redit로 cache data로써 관리과 되고 유저들의 score에 따라 변동 되기 때문에 각각의 값을 체크하기 보다는
        None과 각 Type을 체크한다
        해당 유저에 값은 똑같은지 체크
        """
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for ranking_data in response_data['top_ranker_info_list']:
            self.assertEqual(type(ranking_data['rank']), int)
            self.assertEqual(type(ranking_data['nickname']), str)
            self.assertEqual(type(ranking_data['total_score']), int)

            if ranking_data['account'] == 'test-user1':
                self.assertEqual(ranking_data, response_data['my_ranking'])

    def test_sucess_searching_ranking_with_access_token(self):
        """
        잘몬된 token을 주고 자격인증 실패 반화 (401)
        """
        access_token = self.return_access_token('test-user1', 'testPassword1!')

        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}wrong"}
        response = self.client.get(self.url, content_type='application/json', **headers)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['code'], 'token_not_valid')
