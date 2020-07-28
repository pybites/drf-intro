from rest_framework import generics
from rest_framework import permissions

from .models import Pomodoro
from .permissions import IsOwnerOrReadOnly
from .serializers import PomodoroSerializer


class PomodoroList(generics.ListCreateAPIView):
    queryset = Pomodoro.objects.all()
    serializer_class = PomodoroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PomodoroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pomodoro.objects.all()
    serializer_class = PomodoroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
