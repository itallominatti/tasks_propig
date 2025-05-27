from rest_framework import serializers

class CreateTaskRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    users = serializers.ListField(
        child=serializers.UUIDField(), required=False, allow_empty=True
    )

class CreateTaskResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    links = serializers.DictField(child=serializers.JSONField(), required=False)