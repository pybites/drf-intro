from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import permissions

from .models import Pomodoro
from .permissions import IsOwnerOrReadOnly, AccountPermissions
from .serializers import PomodoroSerializer, UserSerializer


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


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AccountPermissions]

    def get_queryset(self):
        """don't show all users unless super user"""
        users = User.objects.all()
        if self.request.user.is_superuser:
            return users
        return users.filter(username=self.request.user.username)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AccountPermissions]
