from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        
# Serializer específico para criação de usuário com senha tratada
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'full_name']

    def create(self, validated_data):
        # Utiliza create_user para gerar o hash seguro da senha
        user = CustomUser.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', '')
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Adiciona os dados do usuário na resposta do Login
        data['user'] = UserSerializer(self.user).data
        data['token'] = data.pop('access') # Renomeia 'access' para 'token' (padrão que usamos no React)
        return data