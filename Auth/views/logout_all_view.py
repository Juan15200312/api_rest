from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class LogoutAllView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            tokens = OutstandingToken.objects.filter(user=request.user)
            for outstanding in tokens:
                try:
                    RefreshToken(outstanding.token).blacklist()
                except TokenError:
                    continue
            return Response({'message': 'Sesiones cerradas correctamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Error al cerrar las sesiones',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)