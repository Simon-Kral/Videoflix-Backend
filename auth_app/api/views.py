from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.utils.http import urlsafe_base64_decode
from ..models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from ..utils import send_activation_email, send_reset_password_email
from django.shortcuts import redirect


class RegistrationView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            send_activation_email(saved_account)
            return Response({
                'token': token.key,
                'user_id': saved_account.pk,
                'email': saved_account.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """ 
    Allows authenticated users to view or update their own profile information.
    """
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data})


@api_view(['GET'])
@permission_classes([AllowAny])
def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
                account_activation = 'activation_successful'
            else:
                account_activation = 'already_activated'
        else:
            account_activation = 'invalid'
    except:
        account_activation = 'no_user'
    return redirect(f'http://localhost:4200/login/?activation={account_activation}')


class ForgotPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        user = CustomUser.objects.get(email=request.data['email'])

        if user:
            send_reset_password_email(user)
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        return Response({'message': 'user does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def reset_password(request, uidb64, token):

    uid = urlsafe_base64_decode(uidb64).decode()
    user = CustomUser.objects.get(pk=uid)

    if request.method == 'GET':
        if default_token_generator.check_token(user, token):
            return redirect(f'http://localhost:4200/reset-password/?uidb64={uidb64}&token={token}')

    if request.method == 'POST':
        try:
            password = request.data['password']
            repeated_password = request.data['repeated_password']
            if default_token_generator.check_token(user, token):
                if password == repeated_password:
                    user.set_password(request.data['password'])
                    user.save()
                    return Response({'message': 'reset_successful'}, status=status.HTTP_200_OK)
                else:
                    error = 'passwords'
            else:
                error = 'invalid'
        except:
            error = 'no_user'
        return Response({'message': error}, status=status.HTTP_400_BAD_REQUEST)
