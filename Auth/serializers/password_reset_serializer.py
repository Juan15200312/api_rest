from rest_framework import serializers
from Auth.models import PasswordReset


class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = ['user', 'code_hash', 'request_ip']

    def validate(self, attrs):
        if self.instance and attrs.get('user'):
            raise serializers.ValidationError({'user': 'Se necesita de un usuario para crear el token.'})
        if self.instance and attrs.get('request_ip'):
            raise serializers.ValidationError({'request_ip': 'Se necesita un ip para crear el token.'})

        return attrs

    def create(self, validated_data):
        password_reset = PasswordReset(**validated_data)
        password_reset.save()
        return password_reset

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': instance.user.first_name,
            'request_ip': instance.request_ip,
            'created_at': instance.created_at,
        }
