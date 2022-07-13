import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from user.models import User


class SignUpTest(APITestCase):
    """회원가입 테스트

    Writer: 전기원
    Date: 2022-07-13

    """
 
    def test_create_signup(self):
        """
        회원가입 성공 테스트입니다.
        """
        client = APIClient()
        url = '/users/signup'
        data = {'account':'chacha','password':'chacha1234','nickname':'chachacha'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"message": "회원가입이 완료 되었습니다."})   
        self.assertEqual(User.objects.filter(account='chacha').exists(), True)

        
    def test_fail_create_signup_with_wrong_password(self):
        """
        비밀번호를 잘못 구성한 실패 테스트입니다.
        """  
        client = APIClient()
        url = '/users/signup'
        data = {'account':'hoho','password':'hoho','nickname':'hohoho'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['비밀번호는 8~15자의 영소문자와 숫자로 이루어져야합니다.']})

        
    def test_fail_create_signup_with_existed_account(self):
        """
        이미 있는 account로 가입을 시도한 실패 테스트입니다.
        """
        self.user = User.objects.create(account='testtest', password='signup1234', nickname='toto')
        client = APIClient()
        url = '/users/signup'
        data = {'account':'testtest','password':'test12345','nickname':'testtest'}

        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'account': ['user의 account은/는 이미 존재합니다.']})

    def test_fail_create_signup_with_existed_nickname(self):
        """
        이미 있는 닉네임으로 가입을 시도한 실패 테스트입니다.
        """
        self.user = User.objects.create(account='testtest', password='signup1234', nickname='toto')
        client = APIClient()
        url = '/users/signup'
        data = {'account':'test','password':'test12345','nickname':'toto'}

        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'nickname': ['user의 nickname은/는 이미 존재합니다.']})
