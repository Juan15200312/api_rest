from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from Auth.models import generar_token
from Auth.serializers import PasswordResetSerializer
from Users.models import User
from django.conf import settings
from Users.serializers import UserSerializer
from services import send_email


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email') or ''

        if email != '':
            user = User.objects.filter(email=email).first()
            if user:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    request_ip = x_forwarded_for.split(',')[0]
                else:
                    request_ip = request.META.get('REMOTE_ADDR')
                token, code_hash = generar_token()
                serializer = PasswordResetSerializer(data={
                    'user': user.id,
                    'code_hash': code_hash,
                    'request_ip': request_ip,
                })
                if serializer.is_valid():
                    serializer.save()
                    print(token)
                    email_context = {'user': UserSerializer(user).data, 'code':{'1': token[:3], '2': token[3:6], '3': token[6:9]}}
                    send_email(template_name=settings.TEMPLATES_EMAIL['reset_password'], context=email_context,
                               to_email='juanjoseortizolivares@gmail.com', subject='Bienvenido')
                    return Response({'message': 'Si existe un usuario, se envio el correo de recuperación'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Si existe un usuario, se envio el correo de recuperación'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Email requerido'}, status=status.HTTP_400_BAD_REQUEST)


