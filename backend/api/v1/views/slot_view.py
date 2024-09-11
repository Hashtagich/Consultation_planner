from api.v1.serializers.slot_serializer import (SlotSerializerForPOST, SlotSerializerForGET, CommentSerializer,
                                                SlotSerializerForCancel)
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from schedule.models import Slot, Comment
from users.permissions import IsNotBlocked


@extend_schema(tags=['Слоты'])
class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()

    permission_classes = [IsAuthenticated, IsNotBlocked]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SlotSerializerForGET
        else:
            return SlotSerializerForPOST

    def check_role(self):
        user = self.request.user
        return user.role.title == 'Специалист'

    @extend_schema(summary="API для получения всех слотов")
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role.title == 'Клиент':
            free_slots = Slot.objects.filter(status='free')
            reserved_slots = Slot.objects.filter(client=user, status='reserved')
            slots = free_slots | reserved_slots
        elif self.check_role():
            slots = Slot.objects.filter(specialist=user, status__in=['free', 'reserved'])
        else:
            slots = Slot.objects.none()

        serializer = self.get_serializer(slots, many=True)
        return Response(serializer.data)

    @extend_schema(summary="API для получения конкретного слота по ID")
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()

        client_access = instance.client == user and instance.status in ('free', 'reserved')
        specialist_access = instance.specialist == user

        if client_access or specialist_access:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        else:
            return Response({'error': 'У вас нет доступа к этому слоту.'}, status=403)

    @extend_schema(summary="API для создания слота")
    def create(self, request, *args, **kwargs):
        if self.check_role():
            return super().create(request, *args, **kwargs)
        return Response({'error': 'У вас нет прав для создания слотов.'}, status=403)

    @extend_schema(summary="API для удаления слота")
    def destroy(self, request, *args, **kwargs):
        if self.check_role():
            return super().destroy(request, *args, **kwargs)
        return Response({'error': 'У вас нет прав для удаления слотов.'}, status=403)

    @extend_schema(summary="API для редактирования слота")
    def partial_update(self, request, *args, **kwargs):
        if self.check_role():
            return super().partial_update(request, *args, **kwargs)
        return Response({'error': 'У вас нет прав для редактирования слотов.'}, status=403)

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response({'error': 'Метод обновления недоступен.'}, status=405)

    @extend_schema(summary="API для отмены резервирования слота")
    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        slot = self.get_object()

        if slot.client != request.user and slot.status != 'reserved':
            return Response({'detail': 'Вы не имеете прав для отмены этого слота.'}, status=status.HTTP_403_FORBIDDEN)

        slot.change_status()
        slot.save()

        comment_data = request.data.get('comment', {})
        if comment_data:
            comment = Comment(
                text=comment_data.get('text', None),
                reason=comment_data.get('reason', 'None'),
                client=request.user,
                slot=slot
            )
            comment.save()

        return Response({"detail": "Консультация отменена и добавлен комментарий."}, status=status.HTTP_200_OK)

    @extend_schema(summary="API для резервирования слота")
    @action(detail=True, methods=['patch'])
    def reserve(self, request, pk=None):
        slot = self.get_object()
        user = request.user

        if slot.status == 'reserved' or slot.client is not None:
            return Response({'detail': 'Слот уже зарезервирован.'}, status=status.HTTP_400_BAD_REQUEST)

        slot.client = user
        slot.change_status(status='reserved')
        slot.save()

        return Response({"detail": "Консультация зарезервирована."}, status=status.HTTP_201_CREATED)
