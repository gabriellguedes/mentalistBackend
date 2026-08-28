from django.db import models
from django.conf import settings

class StudySession(models.Model):
    timer_type = models.CharField(max_length=50)
    duration_minutes = models.IntegerField()
    status = models.CharField(max_length=20, default='completed') # completed | interrupted
    technique_used = models.CharField(max_length=100, blank=True, null=True)
    room_id = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AIPrompt(models.Model):
    category_goal = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    prompt_template = models.TextField()
    recommended_tools = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Technique(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    what_it_is = models.TextField(blank=True, null=True)
    how_it_works = models.TextField(blank=True, null=True)
    recommended_ai_prompt = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class StudyRoom(models.Model):
    name = models.CharField(max_length=255)
    invite_code = models.CharField(max_length=50, blank=True, null=True)
    host_user_id = models.CharField(max_length=100, blank=True, null=True)
    current_timer_status = models.JSONField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RoomParticipant(models.Model):
    room_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    is_focusing = models.BooleanField(default=False)
    status_text = models.CharField(max_length=255, blank=True, null=True)
    week_minutes = models.IntegerField(default=0)
    last_ping = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RoomMessage(models.Model):
    room_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)