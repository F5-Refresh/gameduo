from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import User


class LoginSerializer(serializers.Serializer):

    user_id = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        password = attrs.get('password')

        if user_id and password:
            if User.objects.filter(user_id=user_id).exists():
                user = authenticate(request=self.context.get('request'), user_id=user_id, password=password)

            else:
                msg = {'detail': 'user_id is not registered.', 'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
