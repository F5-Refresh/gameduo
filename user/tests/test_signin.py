from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User


class LoginOUTUserTest(APITestCase):

    """
    로그인, 로그아웃, JWT 발급 테스트 코드

    Writer: 남효정
    Date: 2022-07-13

    로그인: [POST] /users/login/
    로그아웃: [POST] /users/logout/

    dj-rest-auth 사용으로 자동으로 생성된 url입니다. (후행슬래시 존재)
    """

    def setUp(self):

        """
        초기 세팅을 위한 데이터들입니다.
        """

        # 회원가입을 위한 데이터입니다.
        self.data = {'account': 'testcase1', 'nickname': 'testcase1', 'password': 'testcase1'}

        # 로그인을 위한 데이터입니다. (유효한 데이터)
        self.success_data = {'account': 'testcase1', 'password': 'testcase1'}

        # 존재하지 않는 유저의 데이터입니다. (account 불일치)
        self.fail_data_1 = {'account': 'wrong_account', 'password': 'testcase1'}

        # 유저는 존재하나 비밀번호가 일치하지 않는 데이터입니다. (password 불일치)
        self.fail_data_2 = {'account': 'testcase1', 'password': 'wrong_password'}

        # 유저를 생성합니다.
        self.user = User.objects.create_user(**self.data)

    def test_success_login(self):

        """
        [성공] status_code = 200

        self.success_data(유효한 데이터)로 테스르를 진행합니다.
        로그인 시 access_token, refresh_token이 잘 발급되었는지 확인합니다.
        """

        response = self.client.post('/users/login/', self.success_data)

        # access_token, refresh_token이 잘 발급되었는지 확인합니다.
        self.assertTrue(response.data['access_token'])
        self.assertTrue(response.data['refresh_token'])

        # 로그인된 유저가 가입된 회원 아이디와 일치하는지 확인합니다.
        self.assertEqual(response.data['user']['account'], self.success_data['account'])

        # 성공한 로그인의 상태코드가 일치하는지 확인합니다. (200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_login_wrong_account(self):

        """
        [실패] status_code = 400
        {'detail': [ErrorDetail(string='등록되지 않은 사용자입니다.', code='invalid')]}

        self.fail_data_1(존재하지 않는 유저)로 테스트를 진행합니다.
        """

        response = self.client.post('/users/login/', self.fail_data_1)

        # 실패한 로그인의 상태코드가 일치하는지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 실패한 로그인의 상태메세지가 일치하는지 확인합니다.
        self.assertEqual(response.data['detail'][0], '등록되지 않은 사용자입니다.')

    def test_fail_login_wrong_password(self):

        """
        [실패] status_code = 400
        {'detail': [ErrorDetail(string='올바른 패스워드가 아닙니다.', code='invalid')]}

        self.fail_data_2(비밀번호 불일치)로 테스트를 진행합니다.
        """

        response = self.client.post('/users/login/', self.fail_data_2)

        # 실패한 로그인의 상태코드가 일치하는지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 실패한 로그인의 상태메세지가 일치하는지 확인합니다.
        self.assertEqual(response.data['detail'][0], '올바른 패스워드가 아닙니다.')

    def test_success_logout(self):

        """
        [성공] status_code = 200
        {'detail': '로그아웃되었습니다.'}

        self.success_data에 유효한 refresh_token을 넣어서 로그아웃을 테스트합니다.
        """

        response = self.client.post('/users/login/', self.success_data)
        refresh_token = response.data['refresh_token']
        self.success_data['refresh'] = refresh_token

        response = self.client.post('/users/logout/', self.success_data)

        # 성공한 로그아웃의 상태코드가 일치하는지 확인합니다. (200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 성공한 로그아웃의 상태메세지가 일치하는지 확인합니다.
        self.assertEqual(response.data['detail'], '로그아웃되었습니다.')

    def test_fail_logout(self):

        """
        [실패] status_code = 500
        {'detail': 'An error has occurred.'}

        올바르지 않은 refresh_token을 넣어서 로그아웃을 테스트합니다.
        """

        response = self.client.post('/users/login/', self.success_data)
        refresh_token = 'wrong_refresh_token'
        self.success_data['refresh'] = refresh_token

        response = self.client.post('/users/logout/', self.success_data)

        # 실패한 로그아웃의 상태코드가 일치하는지 확인합니다. (500)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 실패한 로그아웃의 상태메세지가 일치하는지 확인합니다.
        self.assertEqual(response.data['detail'], 'An error has occurred.')
