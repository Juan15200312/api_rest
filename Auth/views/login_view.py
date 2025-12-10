from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from Users.serializers import UserSerializer


class LoginView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'message': 'Email y contraseña obligatoria'},
                            status=status.HTTP_403_FORBIDDEN)

        user = authenticate(email=email, password=password)

        if user:
            if not user.is_active:
                return Response({'message': 'Cuenta desactivada'},
                                status=status.HTTP_403_FORBIDDEN)

            token_refresh = RefreshToken.for_user(user)
            token_access = token_refresh.access_token
            user_serializer = UserSerializer(user)
            return Response({
                'token_refresh': str(token_refresh),
                'token_access': str(token_access),
                'user': user_serializer.data,
                'message': 'Inicio sesión exitosamente',
            }, status=status.HTTP_200_OK)

        return Response({'message': 'Email o contraseña incorrecta'},
                        status=status.HTTP_400_BAD_REQUEST)
