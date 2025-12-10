from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from Users.serializers import UserSerializer


class UserModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all().filter(is_active=True)
