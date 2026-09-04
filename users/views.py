from rest_framework import viewsets, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, status, generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.authtoken.views import ObtainAuthToken
from .models import CustomUser
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, RegisterSerializer
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login_view(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Valida o token JWT do Google
        user_info = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)
        
        email = user_info.get('email')
        full_name = user_info.get('name', '')
        avatar_url = user_info.get('picture', '')

        if not email:
            return Response({'error': 'O Google não forneceu um e-mail válido.'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Tenta buscar o usuário pelo e-mail
        user = CustomUser.objects.filter(email=email).first()

        # 2. Se não existir, cria o usuário garantindo todos os campos obrigatórios
        if not user:
            # Garante um username válido baseado no e-mail
            base_username = email.split('@')[0]
            username = base_username

            # Garante username único caso já exista
            count = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{count}"
                count += 1

            user = CustomUser.objects.create(
                email=email,
                username=username,
                full_name=full_name,
            )
            # Define o avatar se o seu model possuir esse campo
            if hasattr(user, 'avatar_url'):
                user.avatar_url = avatar_url
                user.save(update_fields=['avatar_url'])

            # Define uma senha inutilizável (pois o login é via OAuth)
            user.set_unusable_password()
            user.save()

        # 3. Gera o token JWT para a aplicação
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'token': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)

    except ValueError:
        return Response({'error': 'Token do Google inválido.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user

    if not user.is_authenticated:
        return Response({'error': 'Não autenticado.'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        return Response({
            "id": str(user.id),
            "username": getattr(user, 'username', ''),
            "email": getattr(user, 'email', ''),
            "full_name": getattr(user, 'full_name', ''),
            "birth_date": getattr(user, 'birth_date', ''),
            "avatar_url": getattr(user, 'avatar_url', ''), 
            "total_focus_minutes": getattr(user, 'total_focus_minutes', 10.0),
        })
        
    elif request.method == 'PATCH':
        total = request.data.get('total_focus_minutes')
        avatar_url = request.data.get('avatar_url')
        
        updated_fields = []
        if total is not None and hasattr(user, 'total_focus_minutes'):
            user.total_focus_minutes = total
            updated_fields.append('total_focus_minutes')
            
        if avatar_url is not None and hasattr(user, 'avatar_url'):
            user.avatar_url = avatar_url
            updated_fields.append('avatar_url')

        if updated_fields:
            user.save(update_fields=updated_fields)

        return Response({
            "id": str(user.id),
            "avatar_url": getattr(user, 'avatar_url', ''),
            "total_focus_minutes": getattr(user, 'total_focus_minutes', 0.0),
        }, status=status.HTTP_200_OK)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

     # Atualizar dados do próprio perfil (Nome, CPF, Data de Nascimento, Avatar)
    @action(detail=False, methods=['patch'], url_path='update-profile')
    def update_profile(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Desativar/Excluir a conta do usuário
    @action(detail=False, methods=['post'], url_path='deactivate-account')
    def deactivate_account(self, request):
        user = request.user
        # Desativa a conta em vez de apagar do banco (Boa prática)
        user.is_active = False
        user.save()
        return Response({'message': 'Conta desativada com sucesso.'}, status=status.HTTP_200_OK)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_username(request, username):
    try:
        user = CustomUser.objects.get(username=username, is_active=True)
        return Response({
            "id": str(user.id),
            "username": user.username,
            "full_name": getattr(user, 'full_name', ''),
            "avatar_url": getattr(user, 'avatar_url', ''),
            "total_focus_minutes": getattr(user, 'total_focus_minutes', 0.0),
            # NOTA: Não expor campos sensíveis como CPF ou data de nascimento para terceiros!
        })
    except CustomUser.DoesNotExist:
        return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)