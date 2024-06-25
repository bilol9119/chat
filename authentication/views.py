from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.hashers import make_password

from .models import User, OTP
from .serializers import UserSerializer
from .utils import validate_password, send_otp_via_email


class AuthenticationViewSet(ViewSet):
    def token(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(username=data.get('username')).first()
        if not user:
            return Response(data={"error": "user not found ", 'ok': False},
                            status=status.HTTP_404_NOT_FOUND)

        if not user.is_verified:
            return Response(data={"Error": "user is not verified", 'ok': False},
                            status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(data.get('password')):
            token = RefreshToken.for_user(user)
            return Response(data={'access': str(token.access_token),
                                  'refresh': str(token)}, status=status.HTTP_200_OK)
        return Response(data={"error": "password is incorrect", 'ok': False},
                        status=status.HTTP_400_BAD_REQUEST)

    def register(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.is_verified:
            return Response(data={"error": "You already registered"}, status=status.HTTP_400_BAD_REQUEST)

        if user:
            serializer = UserSerializer(user, data={'password': make_password(password)}, partial=True)
        else:
            serializer = UserSerializer(data={"email": email, "password": make_password(password)})

        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)

        if validate_password(password):
            otp_obj = OTP.objects.create(otp_user=serializer.instance)
            otp_obj.save()
            if not send_otp_via_email(email, otp_obj.otp_code):
                otp_obj.delete()
                return Response({"error": "Error while sending otp code!"}, status.HTTP_400_BAD_REQUEST)
            return Response({"otp_key": otp_obj.otp_key}, status=status.HTTP_200_OK)
        return Response({"error": "please enter valid password"})

    def verify_register(self, request, *args, **kwargs):
        otp_key = request.data.get('otp_key')
        otp_code = request.data.get('otp_code')

        otp_obj = OTP.objects.filter(otp_key=otp_key).first()
        if not otp_obj:
            return Response({"error": "Otp key is not found"}, status.HTTP_400_BAD_REQUEST)

        if otp_obj.otp_attempt > 2:
            return Response({"error": "Please try later"}, status.HTTP_400_BAD_REQUEST)

        if otp_obj.otp_code == otp_code:
            user = User.objects.filter(id=otp_obj.otp_user.id).first()
            user.is_verified = True
            user.save(update_fields=['is_verified'])
            return Response({"detail": "Successfully verified!"}, status.HTTP_200_OK)

        otp_obj.otp_attempt += 1
        otp_obj.save(update_fields=['otp_attempt'])
        return Response({"error": "Otp code is wrong"}, status.HTTP_400_BAD_REQUEST)