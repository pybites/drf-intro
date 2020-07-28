from rest_framework import serializers

from .models import Pomodoro


class PomodoroSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Pomodoro
        fields = ['added', 'notes', 'user']
