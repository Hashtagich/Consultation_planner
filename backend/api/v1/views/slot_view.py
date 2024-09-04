from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from schedule.models import Slot
from api.v1.serializers.slot_serializer import SlotSerializer


class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    # permission_classes = [IsAuthenticated]  # Только для аутентифицированных пользователей

    def check_role(self):
        user = self.request.user
        return user.role.title == 'Специалист'

    def get_queryset(self):
        # return self.queryset
        user = self.request.user
        if user.role.title == 'Клиент':
            return Slot.objects.filter(client=user)  # Клиент видит только свои слоты
        elif self.check_role():
            return Slot.objects.filter(specialist=user)  # Специалист видит свои слоты
        return Slot.objects.none()  # Для других ролей ничего не возвращаем

    def create(self, request, *args, **kwargs):
        if request.user.role.title == 'Специалист':
            return super().create(request, *args, **kwargs)
        return Response({'error': 'У вас нет прав для создания слотов.'}, status=403)

    # def update(self, request, *args, **kwargs):
    #     if request.user.role.title == 'Специалист':
    #         return super().update(request, *args, **kwargs)
    #     return Response({'error': 'У вас нет прав для изменения слотов.'}, status=403)
    #
    # def destroy(self, request, *args, **kwargs):
    #     if request.user.role.title == 'Специалист':
    #         return super().destroy(request, *args, **kwargs)
    #     return Response({'error': 'У вас нет прав для удаления слотов.'}, status=403)
