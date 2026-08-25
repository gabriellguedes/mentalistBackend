from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_date = serializers.DateTimeField(source='created_at', read_only=True)
    updated_date = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'role', 'full_name', 'avatar_url',
            'total_focus_minutes', 'current_level', 'badges',
            'settings', 'created_date', 'updated_date'
        ]