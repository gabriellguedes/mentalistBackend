from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from .models import CustomUser
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, RegisterSerializer


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user

    # Se estiver autenticado
    if request.method == 'GET':
        return Response({
            "id": str(user.id),
            "username": user.username,
            "email": getattr(user, 'email', ''),
            "full_name": user.full_name,
            "total_focus_minutes": getattr(user, 'total_focus_minutes', 0.0),
        })
        
    elif request.method == 'PATCH':
        total = request.data.get('total_focus_minutes')
        if total is not None and hasattr(user, 'total_focus_minutes'):
            user.total_focus_minutes = total
            user.save(update_fields=['total_focus_minutes'])
        return Response({
            "id": str(user.id),
            "total_focus_minutes": getattr(user, 'total_focus_minutes', 0.0),
        }, status=status.HTTP_200_OK)
    
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Gera o token JWT para já logar o usuário automaticamente após o cadastro
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data

        return Response({
            'user': user_data,
            'token': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)