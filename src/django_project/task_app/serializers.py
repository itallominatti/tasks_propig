from rest_framework import serializers

class MetaOutputSerializer(serializers.Serializer):
    total_tasks = serializers.IntegerField()
    current_page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    query_params = serializers.DictField(child=serializers.JSONField(), required=False)

class TaskOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    users = serializers.ListField(
        child=serializers.UUIDField(), required=False, allow_empty=True
    )
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

class CreateTaskRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    users = serializers.ListField(
        child=serializers.UUIDField(), required=False, allow_empty=True
    )

class CreateTaskResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    links = serializers.DictField(child=serializers.JSONField(), required=False)

class TaskListResponseSerializer(serializers.Serializer):
    data = TaskOutputSerializer(many=True)
    meta = MetaOutputSerializer(required=False)
    links = serializers.DictField(child=serializers.JSONField(), required=False)