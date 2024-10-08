from api.v1.serializers.slot_serializer import (SlotSerializerForPOST, SlotSerializerForGET, CommentSerializer)
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from schedule.models import Slot
from schedule.tasks import send_email, send_slot_notification
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
            slots = Slot.objects.filter(specialist=user, status__in=['free', 'reserved', 'agreement'])
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
            return Response({'error': 'У вас нет доступа к этому слоту.'}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(summary="API для создания слота")
    def create(self, request, *args, **kwargs):
        if not self.check_role():
            return Response({'error': 'У вас нет прав для создания слотов.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = SlotSerializerForPOST(data=request.data)
        if serializer.is_valid():
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            specialist = request.user

            existing_slots = Slot.objects.filter(
                specialist=specialist,
                start_time=start_time,
                end_time=end_time
            )
            if existing_slots.exists():
                return Response({'error': 'Слот с такими датами уже существует.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(specialist=request.user)
            return Response({'message': 'Слот успешно создан!', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response({'error': 'Ошибка валидации', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="API для удаления слота")
    def destroy(self, request, *args, **kwargs):
        if self.check_role():
            return super().destroy(request, *args, **kwargs)
        return Response({'error': 'У вас нет прав для удаления слотов.'}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(summary="API для редактирования слота")
    def partial_update(self, request, *args, **kwargs):
        if self.check_role():
            return super().partial_update(request, *args, **kwargs)
        return Response({'error': 'У вас нет прав для редактирования слотов.'}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response({'error': 'Метод обновления недоступен.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(
        summary="API для отмены резервирования слота клиентом",
        request=CommentSerializer
    )
    @action(detail=True, methods=['patch'])
    def cancel_client(self, request, pk=None):
        slot = self.get_object()

        if slot.client != request.user and slot.status not in ('agreement', 'reserved'):
            return Response({'detail': 'Вы не имеете прав для отмены этой консультации.'},
                            status=status.HTTP_403_FORBIDDEN)

        comment_data = request.data
        comment_data['slot'] = slot.id
        comment_data['client'] = request.user.id

        comment_serializer = CommentSerializer(data=comment_data)

        if comment_data and comment_serializer.is_valid():
            comment_serializer.save(client=request.user)
        elif comment_data:
            return Response({'error': 'Ошибка валидации комментария', 'details': comment_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        title = f'Отмена консультации {slot.start_time.strftime("%d.%m.%Y")} в {slot.start_time.strftime("%H:%M")}'
        message = f'Клиент {slot.client} отменил консультацию на {slot.start_time.strftime("%d.%m.%Y")} {slot.start_time.strftime("%H:%M")} - {slot.end_time.strftime("%H:%M")}'
        sub_list = slot.specialist.email

        slot.change_status()
        slot.save()

        send_email(title, message, sub_list)

        return Response({"detail": "Консультация отменена и добавлен комментарий."}, status=status.HTTP_200_OK)

    @extend_schema(summary="API для резервирования слота клиентом")
    @action(detail=True, methods=['patch'])
    def reserve(self, request, pk=None):
        slot = self.get_object()
        user = request.user

        if slot.status != 'free' or slot.client is not None:
            return Response({'detail': 'Консультация уже зарезервирован.'}, status=status.HTTP_400_BAD_REQUEST)

        slot.client = user
        slot.change_status(status='agreement')
        slot.save()

        title = f'Заявка на согласование консультации на {slot.start_time.strftime("%d.%m.%Y")} в {slot.start_time.strftime("%H:%M")}'
        message = f'Клиент {user} отправил на согласование консультацию на {slot.start_time.strftime("%d.%m.%Y")} {slot.start_time.strftime("%H:%M")} - {slot.end_time.strftime("%H:%M")}'
        sub_list = slot.specialist.email
        send_email(title, message, sub_list)

        return Response({"detail": "Резервирование консультации отправлено на согласование специалисту."},
                        status=status.HTTP_201_CREATED)

    @extend_schema(summary="API для отмены резервирования слота специалистом")
    @action(detail=True, methods=['patch'])
    def cancel_specialist(self, request, pk=None):
        slot = self.get_object()
        user = slot.client

        if slot.specialist != request.user or slot.status != 'agreement':
            return Response({'detail': 'Вы не имеете прав для отмены этого слота.'}, status=status.HTTP_403_FORBIDDEN)

        send_slot_notification(slot, user, action="Отмена")
        slot.change_status()
        slot.save()

        return Response({"detail": "Консультация не согласована, письмо/уведомление отправлено клиенту."},
                        status=status.HTTP_200_OK)

    @extend_schema(summary="API для согласования слота специалистом")
    @action(detail=True, methods=['patch'])
    def agree(self, request, pk=None):
        slot = self.get_object()
        user = request.user
        if slot.specialist != request.user or slot.status != 'agreement':
            return Response({'detail': 'Вы не имеете прав для согласования этого слота.'},
                            status=status.HTTP_403_FORBIDDEN)

        slot.change_status(status='reserved')
        slot.save()
        send_slot_notification(slot, user, action="Согласование")

        return Response({"detail": "Консультация согласована специалистом, письмо/уведомление отправлено клиенту."},
                        status=status.HTTP_201_CREATED)
