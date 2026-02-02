from http.client import responses

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.conf import settings
from rest_framework import viewsets
from .models import Run
from .serializers import RunSerializer, UserSerializer


# Create your views here.
@api_view(['GET'])
def company_details(request):
    details = {'company_name': settings.COMPANY_NAME,
               'slogan': settings.COMPANY_SLOGAN,
               'contacts': settings.COMPANY_CONTACTS}
    return Response(details)

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        qs = self.queryset.filter(is_superuser=False)

        user_type = self.request.query_params.get('type')
        if user_type == 'coach':
            qs = qs.filter(is_staff=True)
        elif user_type == 'athlete':
            qs = qs.filter(is_staff=False)
        return qs


class StartRunView(APIView):

    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status == 'finished' or run.status == 'in_progress':
            return Response(self, status=status.HTTP_400_BAD_REQUEST)
        else:
            run.status = 'in_progress'
            run.save()
            return Response(run.status, status=status.HTTP_200_OK)



class StopRunView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status == 'init' or run.status == 'finished':
            return Response(self, status=status.HTTP_400_BAD_REQUEST)
        else:
            run.status = 'finished'
            run.save()
            return Response(run.status, status=status.HTTP_200_OK)
