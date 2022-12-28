from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """ create new user with encrypted password and return it """
        password = validated_data.pop('password', None)
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super(UserSerializer, self).update(instance, validated_data)
        print("hellklkk")
        print(password)
        if password:
            user.set_password(password)
            user.save()
        return user




class AuthTokenSerializer(serializers.Serializer):
    """serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _("authentication failed")
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs
