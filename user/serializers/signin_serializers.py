from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from user.models import User


class LoginSerializer(serializers.Serializer):

    account = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = User.objects.filter(account=data.get('account')).first()

        if not user:
            raise ValidationError({'detail': '등록되지 않은 사용자입니다.'})

        if not user.check_password(data['password']):
            raise ValidationError({'detail': '올바른 패스워드가 아닙니다.'})

        return data
