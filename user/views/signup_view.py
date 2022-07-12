from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers.signup_serializers import SignUpSerializer


class SignUpView(APIView):

    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=SignUpSerializer, responses={201: SignUpSerializer})
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'회원가입이 완료 되었습니다.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
