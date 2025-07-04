from rest_framework import serializers
from .models import NetworkParticipant


class NetworkParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkParticipant
        fields = "__all__"
        read_only_fields = ["debt_to_supplier", "type"]  # запретить изменение полей


