from django.shortcuts import render

from rest_framework.views import APIView
from .serializers import MessageSerializer
from normal.models import Message
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated



class AddMessage(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(user = self.request.user)


class MessageOperation(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(MessageOperation, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user, pk=int(self.kwargs.get("pk")))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        all_data = dict(request.data)
        serializer = self.get_serializer(instance, data=all_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



