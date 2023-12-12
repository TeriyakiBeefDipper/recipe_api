from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _


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
        user = get_user_model().objects.create_user(email=email, password=password, name=name)  # noqa
        # user.set_password(password)    # this should be redundant
        return user

    def update(self, instance, validated_data):
        """update and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': "password"}, trim_whitespace=False)  # noqa

    def validate(self, attrs):
        """validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'),
                            username=email,
                            password=password)
        if not user:
            msg = _('Unable to authenticate')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
