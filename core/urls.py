from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudySessionViewSet, AIPromptViewSet, TechniqueViewSet,
    StudyRoomViewSet, RoomParticipantViewSet, RoomMessageViewSet
)

router = DefaultRouter()
router.register(r'entities/StudySession', StudySessionViewSet, basename='studysession')
router.register(r'entities/AIPrompt', AIPromptViewSet, basename='aiprompt')
router.register(r'entities/Technique', TechniqueViewSet, basename='technique')
router.register(r'entities/StudyRoom', StudyRoomViewSet, basename='studyroom')
router.register(r'entities/RoomParticipant', RoomParticipantViewSet, basename='roomparticipant')
router.register(r'entities/RoomMessage', RoomMessageViewSet, basename='roommessage')

urlpatterns = [
    path('', include(router.urls)),
]