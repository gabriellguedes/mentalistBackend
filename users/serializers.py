import random
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_date = serializers.DateTimeField(source='created_at', read_only=True)
    updated_date = serializers.DateTimeField(source='updated_at', read_only=True)
    avatar_url = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'role', 'full_name', 'avatar_url', 'cpf', 'birth_date', 'avatar',
            'total_focus_minutes', 'current_level', 'badges',
            'settings', 'created_date', 'updated_date'
        ]
    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return getattr(obj, 'avatar_url', None)
           
# Serializer específico para criação de usuário com senha tratada
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'full_name', 'username', 'cpf', 'birth_date']

    def create(self, validated_data):
        raw_username = validated_data.get('username') or validated_data['email'].split('@')[0]
        
        # Garante unicidade adicionando número aleatório se o username já existir
        final_username = raw_username
        while CustomUser.objects.filter(username=final_username).exists():
            random_num = random.randint(100, 9999)
            final_username = f"{raw_username}{random_num}"

        user = CustomUser.objects.create_user(
            username=final_username,
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            cpf=validated_data.get('cpf', None),
            birth_date=validated_data.get('birth_date', None)
        )
        return user
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Adiciona os dados do usuário na resposta do Login
        data['user'] = UserSerializer(self.user).data
        data['token'] = data.pop('access') # Renomeia 'access' para 'token' (padrão que usamos no React)
        return data