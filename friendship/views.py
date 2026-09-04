from django.shortcuts import render
from rest_framework.decorators import action
from .models import Friendship
from .serializers import FriendshipSerializer

class FriendshipViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        # Retorna todas as solicitações envolvendo o usuário autenticado
        return Friendship.objects.filter(
            models.Q(sender=self.request.user) | models.Q(receiver=self.request.user)
        )

    # Enviar pedido de amizade
    def create(self, request, *args, **kwargs):
        receiver_id = request.data.get('receiver_id')
        if not receiver_id:
            return Response({'error': 'ID do destinatário é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if int(receiver_id) == request.user.id:
            return Response({'error': 'Você não pode adicionar a si mesmo.'}, status=status.HTTP_400_BAD_REQUEST)

        receiver = CustomUser.objects.get(id=receiver_id)
        friendship, created = Friendship.objects.get_or_create(
            sender=request.user,
            receiver=receiver,
            defaults={'status': 'pending'}
        )
        if not created:
            return Response({'message': 'Solicitação já existente.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(FriendshipSerializer(friendship).data, status=status.HTTP_201_CREATED)

    # Aceitar solicitação
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friendship = self.get_object()
        if friendship.receiver != request.user:
            return Response({'error': 'Ação não permitida.'}, status=status.HTTP_403_FORBIDDEN)
        
        friendship.status = 'accepted'
        friendship.save()
        return Response({'status': 'Amizade aceita com sucesso.'})

    # Recusar solicitação
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        friendship = self.get_object()
        if friendship.receiver != request.user:
            return Response({'error': 'Ação não permitida.'}, status=status.HTTP_403_FORBIDDEN)

        friendship.status = 'declined'
        friendship.save()
        return Response({'status': 'Solicitação recusada.'})

    # Listar lista de amigos confirmados
    @action(detail=False, methods=['get'])
    def friends_list(self, request):
        user = request.user
        friendships = Friendship.objects.filter(
            (models.Q(sender=user) | models.Q(receiver=user)) & models.Q(status='accepted')
        )
        friends = []
        for f in friendships:
            friends.append(f.receiver if f.sender == user else f.sender)
        
        return Response(UserSerializer(friends, many=True).data)