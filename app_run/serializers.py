from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Run


class UserSerializer(serializers.ModelSerializer):
    type: SerializerMethodField = serializers.SerializerMethodField()
    runs_finished: SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished']


    def get_type(self, obj):
        if obj.is_staff:
            obj.type = 'coach'
        else:
            obj.type = 'athlete'
        return obj.type

    def get_runs_finished(self, obj):
        return Run.objects.filter(athlete=obj, status='finished').count()


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserShortSerializer(read_only=True, source='athlete', )

    class Meta:
        model = Run
        fields = '__all__'