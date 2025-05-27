from rest_framework import serializers

class AuthenticateUserRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AuthenticateUserResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    expires_at = serializers.CharField()