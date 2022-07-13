from datetime import datetime, timedelta

from raid.models import RaidHistory
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient, APITestCase
from user.models import User


class UserSearchTest(APITestCase):
    """유저정보 조회 기능 Test

    Writer: 김동규
    Date: 2022-07-12

    유저정보 조회의 성공/실패 경우를 테스트 합니다.
    """

    maxDiff = None

    def setUp(self):
        self.user = User.objects.create_user(account='test-user1', nickname='user1', password='testPassword1!')

        RaidHistory.objects.create(
            id=1,
            level=0,
            score=20,
            user=self.user,
            end_time=(datetime.now() + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M'),
        )
        RaidHistory.objects.create(
            id=2,
            level=1,
            score=47,
            user=self.user,
            end_time=(datetime.now() + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M'),
        )
        RaidHistory.objects.create(
            id=3,
            level=2,
            score=85,
            user=self.user,
            end_time=(datetime.now() + timedelta(minutes=3)).strftime('%Y-%m-%d %H:%M'),
        )
        RaidHistory.objects.create(id=4, level=2, score=0, user=self.user, end_time=None)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        User.objects.all().delete()
        RaidHistory.objects.all().delete()

    def test_success_user_search(self):
        """
        유저정보 조회 성공 테스트
        method: GET
        """

        url = '/users/search/test-user1'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'nickname': 'user1',
                'total_score': 152,
                'boss_raid_histories': [
                    {
                        'id': 4,
                        'score': 0,
                        'enter_time': (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                        'end_time': None,
                    },
                    {
                        'id': 3,
                        'score': 85,
                        'enter_time': (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                        'end_time': (datetime.now() + timedelta(minutes=3)).strftime('%Y-%m-%d %H:%M'),
                    },
                    {
                        'id': 2,
                        'score': 47,
                        'enter_time': (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                        'end_time': (datetime.now() + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M'),
                    },
                    {
                        'id': 1,
                        'score': 20,
                        'enter_time': (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                        'end_time': (datetime.now() + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M'),
                    },
                ],
            },
        )

    def test_success_user_search_offset_limit(self):
        """
        유저정보 조회 성공 테스트
        method: GET

        offset, limit 조건을 사용하여 원하는 개수의 유저정보를 불러옵니다.
        """

        url = '/users/search/test-user1?offset=0&limit=3'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'nickname': 'user1',
                'total_score': 132,
                'boss_raid_histories': [
                    {
                        'id': 4,
                        'score': 0,
                        'enter_time': (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                        'end_time': None,
                    },
                    {
                        'id': 3,
                        'score': 85,
                        'enter_time': (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                        'end_time': (datetime.now() + timedelta(minutes=3)).strftime('%Y-%m-%d %H:%M'),
                    },
                    {
                        'id': 2,
                        'score': 47,
                        'enter_time': (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                        'end_time': (datetime.now() + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M'),
                    },
                ],
            },
        )

    def test_fail_user_search_due_to_unauthorized_user(self):
        """
        유저정보 조회 실패 테스트
        method: GET

        인증/인가에 실패한 유저는 해당 API 기능을 사용할 수 없습니다.
        인증되지 않은 client 변수를 새롭게 선언하여 의도적으로 인증/인가에 실패하도록 테스트합니다.
        """

        self.client = APIClient()

        url = '/users/search/test-user1'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'})

    def test_fail_user_search_due_to_not_existed_user(self):
        """
        유저정보 조회 실패 테스트
        method: GET

        존재하지 않는 유저의 유저정보는 조회할 수 없습니다.
        """

        url = '/users/search/test-user2'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': '찾을 수 없습니다.'})
