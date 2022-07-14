import time

from django.core.cache import cache
from raid.models import RaidHistory

# Create your tests here.
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from user.models import User


class LoginOUTUserTest(APITestCase):

    """
    Writer: 이동연
    Date: 2022-07-14
    """

    def setUp(self):

        """
        [초기 세팅]
        """

        self.user = User.objects.create_user(
            **{'account': 'testcase1', 'nickname': 'testcase1', 'password': 'testcase1'}
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        cache.set('limit_time', 1)  # 제한시간에 대한 설정을 1초로 낮추었습니다.

    def test_start_boss_raid_success_case(self):

        """
        [뷰 성공케이스]
        다른 유저가 레이드를 진행중이지 않을 경우에 대한 테스트
        """

        cache.set('can_enter', True)
        url = '/raid/start_raid'
        response = self.client.post(url, format='json', data={'level': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': '유저가 레이드에 입장했습니다', 'is_entered': True})

    def test_start_boss_raid_success_case2(self):

        """
        [뷰 성공케이스]
        다른 유저가 레이드를 진행중일 경우에 대한 테스트
        """

        cache.set('can_enter', False)
        url = '/raid/start_raid'
        response = self.client.post(url, format='json', data={'level': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': '다른유저가 이미 레이드에 입장해있습니다.', 'is_entered': False})

    def test_start_boss_raid_fail_case(self):

        """
        [뷰 실패 케이스]
        요청값이 유효하지 않을 경우에 대한 테스트
        """

        cache.set('can_enter', True)
        url = '/raid/start_raid'
        response = self.client.post(url, format='json', data={'level': 153})  # level은 1 ~ 3까지 존재합니다.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['level'], {'detail': '유효한 레벨이 아닙니다.'})

    def test_end_boss_raid_success_case(self):

        """
        [뷰 성공 케이스]
        레이드를 시작 후 제한시간 이내 레이드 종료요청을 보낸 경우에 대한 테스트
        """

        raid_history = RaidHistory.objects.create(
            user=self.user,
            level=1,
        )
        url = '/raid/end_raid'
        response = self.client.post(url, format='json', data={'is_win': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': '레이드가 정상적으로 종료 되었습니다.', 'boss_raid_history_id': raid_history.id})
        self.assertEqual(cache.get('can_enter'), True)

    def test_end_boss_raid_fail_case(self):

        """
        [뷰 실패 케이스]
        레이드를 시작하지않고 레이드 종료요청을 보낸 경우에 대한 테스트
        """

        url = '/raid/end_raid'
        response = self.client.post(url, format='json', data={'is_win': True})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_auto_end_boss_raid(self):

        """
        [기능 테스트]
        제한시간이 지날경우 자동종료에 대한 테스트
        """

        cache.set('can_enter', True)
        url = '/raid/start_raid'
        response = self.client.post(url, format='json', data={'level': 1})
        time.sleep(1)  # 제한시간을 기다리는 처리
        url = '/raid/end_raid'
        response = self.client.post(url, format='json', data={'is_win': True})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
