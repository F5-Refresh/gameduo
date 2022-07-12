import re

from rest_framework import serializers
from user.models import User


class SignUpSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.get('password')
        
    # 비밀번호 8~15자/소문자,숫자 최소하나 사용
    # 정규식 객체를 리턴 
        password_re =re.compile('^(?=.{8,15}$)(?=.*[a-z])(?=.*[0-9]).*$')
        
        if not re.match(password_re, password):
            raise serializers.ValidationError({"password": ["올바른 비밀번호를 입력하세요."]})

        #  validated_data를 기반으로 User객체를 생성
        user = User.objects.create_user(**validated_data)
        return user
        
    class Meta:
        model = User
        fields = ['user_id','password','nickname']
        extra_kwargs = {'password': {'write_only':True}}
        
