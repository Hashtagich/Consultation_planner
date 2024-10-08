from rest_framework import serializers
from schedule.models import Slot, Comment


class SlotSerializerForGET(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    end_time = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')

    class Meta:
        model = Slot
        fields = (
            'specialist',
            'start_time',
            'end_time',
            'context',
            'cost',
            'status',
            'client'
        )


class SlotSerializerForPOST(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    end_time = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')

    class Meta:
        model = Slot
        fields = (
            'start_time',
            'end_time',
            'context',
            'cost',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'reason',
            'text',
            'client',
            'slot'
        )
