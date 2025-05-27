from rest_framework import serializers

class UserResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    is_active = serializers.BooleanField(default=True, required=False)
    links = serializers.DictField(
        child=serializers.CharField(),
        required=False
    )

class CreateUserRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    is_active = serializers.BooleanField(default=True, required=False)

class CreateUserResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)

class ListOutputMetaSerializer(serializers.Serializer):
    total_count = serializers.IntegerField()
    page_size = serializers.IntegerField()
    current_page = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    links = serializers.DictField(
        child=serializers.CharField(),
        required=False
    )


class ListUserResponseSerializer(serializers.Serializer):
    data = UserResponseSerializer(many=True)
    meta = ListOutputMetaSerializer()

class RetrieveUserResponseSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    is_active = serializers.BooleanField()
    links = serializers.DictField(required=False)

class RetrieveUserRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    