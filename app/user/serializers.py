from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """serialize the user object"""
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """create and return a user with encrypted password"""
        email = validated_data.get('email')
        password = validated_data.get('password')
        name = validated_data.get('name')
        user = get_user_model().objects.create_user(email=email,password=password, name=name)
        user.set_password(password)
        return user
