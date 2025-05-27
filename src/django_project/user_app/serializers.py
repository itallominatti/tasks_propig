from rest_framework import serializers

class CreateUserRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    is_active = serializers.BooleanField(default=True, required=False)

class UserResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()