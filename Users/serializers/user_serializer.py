from rest_framework import serializers
from Users.models import User

class UserSerializerEmail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone']

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'phone': instance.phone,
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'birthday', 'address', 'image']

    def validate(self, attrs):
        if self.instance is None and not attrs.get('email'):
            raise serializers.ValidationError({'email': 'El email es obligatoria a crear un usuario'})

        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'La contraseña es obligatoria al crear el usuario'})
        return attrs

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'first_name': instance.first_name or '',
            'last_name': instance.last_name or '',
            'phone': instance.phone,
            'birthday': instance.birthday or '',
            'address': instance.address or '',
            'image': instance.image or '',
        }