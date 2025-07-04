from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from .models import NetworkParticipant
from .permissions import IsActiveEmployee
from .serializers import NetworkParticipantSerializer


class FactoryViewSet(viewsets.ModelViewSet):
    serializer_class = NetworkParticipantSerializer
    queryset = NetworkParticipant.objects.filter(clients__isnull=False).distinct()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]  # Поля для фильтрации
    permission_classes = [IsAuthenticated, IsActiveEmployee]
