import re

from rest_framework import serializers
from user.models import User


# 회원가입 serializer 입니다.
class SignUpSerializer(serializers.ModelSerializer):
    """회원가입 Serializer

    Writer: 전기원
    Date: 2022-07-12

    """

    def create(self, validated_data):
        password = validated_data.get('password')

        # 비밀번호 8~15자/소문자,숫자 최소하나 사용
        # 정규식 객체를 리턴
        password_re = re.compile('^(?=.{8,15}$)(?=.*[a-z])(?=.*[0-9]).*$')

        if not re.match(password_re, password):
            raise serializers.ValidationError({"password": ["비밀번호는 8~15자의 영소문자와 숫자로 이루어져야합니다."]})

        # validated_data를 기반으로 User객체를 생성
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['account', 'password', 'nickname']
        extra_kwargs = {'password': {'write_only': True}}
