from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Run

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type: SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type']


    def get_type(self, obj):
        if obj.is_staff:
            obj.type = 'coach'
        else:
            obj.type = 'athlete'
        return obj.type