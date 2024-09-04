from api.v1.serializers.slot_serializer import (SlotSerializerForPOST, SlotSerializerForGET)
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from schedule.models import Slot


@extend_schema(tags=['Слоты'])
class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()

    # permission_classes = [IsAuthenticated]  # Только для аутентифицированных пользователей

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SlotSerializerForGET
        return SlotSerializerForPOST

    def check_role(self):
        user = self.request.user
        return user.role.title == 'Специалист'

    @extend_schema(summary="API для получения всех слотов")
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role.title == 'Клиент':
            slots = Slot.objects.filter(status='free')
        elif self.check_role():
            slots = Slot.objects.filter(specialist=user, status__in=['free', 'reserved'])
        else:
            slots = Slot.objects.none()

        serializer = self.get_serializer(slots, many=True)
        return Response(serializer.data)

    @extend_schema(summary="API для получения конкретного слота по ID")
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()  # Получаем экземпляр слота по ID

        if user.role.title == 'Клиент' and instance.status != 'free':
            return Response({'error': 'У вас нет доступа к этому слоту.'}, status=403)

        elif self.check_role() and instance.specialist == user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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
