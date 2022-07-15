from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient, APITestCase
from user.models import User


class RaidStatusSearchTest(APITestCase):
    """유저정보 조회 기능 Test

    Writer: 김동규
    Date: 2022-07-15

    보스레이드 상태조회의 성공/실패 경우를 테스트 합니다.
    """

    maxDiff = None

    def setUp(self):
        self.user = User.objects.create_user(account='test-user1', nickname='user1', password='testPassword1!')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        User.objects.all().delete()

    def test_success_raid_status_search(self):
        """
        보스레이드 상태정보 조회 성공 테스트

        method: GET
        """

        url = '/raids/status-search'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('can_enter', response.data)
        self.assertIn('entered_user_id', response.data)

    def test_fail_raid_status_search_due_to_unauthorized_user(self):
        """
        보스레이드 상태정보 조회 실패 테스트
        method: GET

        인증/인가에 실패한 유저는 해당 API 기능을 사용할 수 없습니다.
        인증되지 않은 client 변수를 새롭게 선언하여 의도적으로 인증/인가에 실패하도록 테스트합니다.
        """

        self.client = APIClient()

        url = '/raids/status-search'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
