from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from user.models import User


class LoginSerializer(serializers.Serializer):

    """로그인 serializer

    Writer: 남효정
    Date: 2022-07-12

    라이브러리의 기본 시리얼라이저를 현재 프로젝트의 User 모델에 맞도록 커스텀합니다.
    """

    account = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = User.objects.filter(account=data.get('account')).first()

        if not user:
            raise ValidationError({'detail': '등록되지 않은 사용자입니다.'})

        if not user.check_password(data['password']):
            raise ValidationError({'detail': '올바른 패스워드가 아닙니다.'})

        return data