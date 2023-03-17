from rest_framework.views import APIView
from accounts.serializers import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model
# from allauth.account.views import LoginView

User = get_user_model()


class RegisterAPIView(APIView):
    
    def post(self, request):
        data = {}
        for i in request.data:
            data.update({i:request.data[i]})
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Вы успешно зарегистрировались. Вам отправлено письмо с активацией', status=201)

class ActivationAPIView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response('Успешно', status=200)
        except User.DoesNotExist:
            return Response('Link expired', status=400)

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_reset_password_code()
        return Response('вам отправлено письмо для восстановления пароля')

class ForgotPasswordCompleteAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordComleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('пароль успешно изменён')
