from rest_framework import serializers
from .models import NetworkParticipant

class NetworkParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkParticipant
        fields = '__all__'
        read_only_fields = ['debt_to_supplier', 'type'] # запретить изменение полей

    def validate(self, data):
        # Проверить, что создается только завод
        if self.instance is None and data.get('type') != NetworkParticipant.Types.FACTORY:
            raise serializers.ValidationError('Через этот API можно создавать только заводы')
        return data