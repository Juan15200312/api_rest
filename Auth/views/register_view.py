from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from Users.serializers import UserSerializer, UserSerializerEmail
from services import send_email


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        register_serializer = self.serializer_class(data=request.data)

        if register_serializer.is_valid():
            user = register_serializer
            user.first_name = request.data.get('first_name')
            user = user.save()
            email_context = {'user': UserSerializer(user).data}
            send_email(template_name=settings.TEMPLATES_EMAIL['welcome'], context=email_context,
                       to_email='juanjoseortizolivares@gmail.com', subject='Bienvenido')
            return Response({'message': 'Usuario registrado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


