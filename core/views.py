from rest_framework import viewsets
from .models import StudySession, AIPrompt, Technique, StudyRoom, RoomParticipant, RoomMessage
from .serializers import (
    StudySessionSerializer, AIPromptSerializer, TechniqueSerializer,
    StudyRoomSerializer, RoomParticipantSerializer, RoomMessageSerializer
)

class StudySessionViewSet(viewsets.ModelViewSet):
    queryset = StudySession.objects.all()
    serializer_class = StudySessionSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)

class AIPromptViewSet(viewsets.ModelViewSet):
    queryset = AIPrompt.objects.all()
    serializer_class = AIPromptSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)

class TechniqueViewSet(viewsets.ModelViewSet):
    queryset = Technique.objects.all()
    serializer_class = TechniqueSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)

class StudyRoomViewSet(viewsets.ModelViewSet):
    queryset = StudyRoom.objects.all()
    serializer_class = StudyRoomSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)

class RoomParticipantViewSet(viewsets.ModelViewSet):
    queryset = RoomParticipant.objects.all()
    serializer_class = RoomParticipantSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)

class RoomMessageViewSet(viewsets.ModelViewSet):
    queryset = RoomMessage.objects.all()
    serializer_class = RoomMessageSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)