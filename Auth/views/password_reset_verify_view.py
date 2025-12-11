from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from Auth.models import PasswordReset
from Auth.serializers import PasswordResetSerializer
from Users.models import User
from django.db import transaction
from django.utils import timezone



class PasswordResetVerifyView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email') or ''
        token = request.data.get('token') or ''

        if email != '' and token != '':
            user = User.objects.filter(email=email).first()
            if user:
                password_reset = (
                    PasswordReset.objects.filter(user=user, used=False, expired_at__gt=timezone.now()).order_by(
                        '-created_at').first())
                if password_reset:
                    if check_password(password=token, encoded=password_reset.code_hash):
                        with transaction.atomic():
                            password_reset.used = True
                            password_reset.consumed_at = timezone.now()
                            password_reset.save(update_fields=['used', 'consumed_at'])

                            (PasswordReset.objects.filter(user=user, used=False).update(used=True,
                                                                                        consumed_at=timezone.now()))
                            print(5)
                        return Response({'message': 'Código valido', 'ok': True}, status=status.HTTP_201_CREATED)
                    print(4)
                    return Response({'error': 'Código invalido o expirado'}, status=status.HTTP_400_BAD_REQUEST)
                print(3)
                return Response({'error': 'Código invalido o expirado'}, status=status.HTTP_400_BAD_REQUEST)
            print(2)
            return Response({'error': 'Código invalido o expirado'}, status=status.HTTP_400_BAD_REQUEST)
        print(1)
        return Response({'error': 'Email y token requerido'}, status=status.HTTP_400_BAD_REQUEST)