from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, AuthenticationFailed


class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token_refresh = request.data.get('token_refresh')

        if not token_refresh:
            return Response({'error': 'Token refresh requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            try:
                token = RefreshToken(token_refresh)
                if int(token['user_id']) == request.user.id:
                    token.blacklist()
                    return Response({'message': 'Sesión cerrada exitosamente'}, status=status.HTTP_200_OK)
                return Response({'error': 'Token no pertenece al usuario'}, status=status.HTTP_400_BAD_REQUEST)
            except TokenError, InvalidToken, AuthenticationFailed:
                return Response({'error': 'Token invalido, expirado o errado'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Error al cerrar la sesión',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



