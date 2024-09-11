from api.v1.serializers.user_serializer import MyUserSerializer, MyUserSerializerForGet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User
from users.permissions import IsAdmin


@extend_schema(tags=['Пользователи'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MyUserSerializerForGet
        else:
            return MyUserSerializer

    @extend_schema(summary="API для блокировки пользователя")
    @action(detail=True, methods=['patch'])
    def block_user(self, request, pk=None):
        user = self.get_object()
        user.is_blocked = True
        user.save()
        return Response({"message": f"Пользователь {user} заблокирован."}, status=status.HTTP_200_OK)

    @extend_schema(summary="API для разблокировки пользователя")
    @action(detail=True, methods=['patch'])
    def unblock_user(self, request, pk=None):
        user = self.get_object()
        user.is_blocked = False
        user.save()
        return Response({"message": f"Пользователь {user} разблокирован."}, status=status.HTTP_200_OK)

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response({'error': 'Метод обновления недоступен.'}, status=405)

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return Response({'error': 'Метод создания недоступен.'}, status=405)

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return Response({'error': 'Метод удаления недоступен.'}, status=405)

    @extend_schema(summary="API для получения всех пользователей")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="API для получения конкретного пользователя по ID")
    def retrieve(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="API для редактирования конкретного пользователя по ID")
    def partial_update(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
