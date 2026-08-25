from rest_framework import serializers
from .models import StudySession, AIPrompt, Technique, StudyRoom, RoomParticipant, RoomMessage

class BaseEntitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_date = serializers.DateTimeField(source='created_at', read_only=True)
    updated_date = serializers.DateTimeField(source='updated_at', read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(source='created_by', read_only=True)

class StudySessionSerializer(BaseEntitySerializer):
    class Meta:
        model = StudySession
        fields = ['id', 'timer_type', 'duration_minutes', 'status', 'technique_used', 'room_id', 'created_date', 'updated_date', 'created_by_id']

class AIPromptSerializer(BaseEntitySerializer):
    class Meta:
        model = AIPrompt
        fields = ['id', 'category_goal', 'title', 'prompt_template', 'recommended_tools', 'created_date', 'updated_date', 'created_by_id']

class TechniqueSerializer(BaseEntitySerializer):
    class Meta:
        model = Technique
        fields = ['id', 'title', 'category', 'what_it_is', 'how_it_works', 'recommended_ai_prompt', 'created_date', 'updated_date', 'created_by_id']

class StudyRoomSerializer(BaseEntitySerializer):
    class Meta:
        model = StudyRoom
        fields = ['id', 'name', 'invite_code', 'host_user_id', 'current_timer_status', 'created_date', 'updated_date', 'created_by_id']

class RoomParticipantSerializer(BaseEntitySerializer):
    class Meta:
        model = RoomParticipant
        fields = ['id', 'room_id', 'user_id', 'user_name', 'is_focusing', 'status_text', 'week_minutes', 'last_ping', 'created_date', 'updated_date', 'created_by_id']

class RoomMessageSerializer(BaseEntitySerializer):
    class Meta:
        model = RoomMessage
        fields = ['id', 'room_id', 'user_name', 'text', 'created_date', 'updated_date', 'created_by_id']