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
from .models import Run, AthleteInfo
from .serializers import RunSerializer, UserSerializer, AthleteInfoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination


# Create your views here.
@api_view(['GET'])
def company_details(request):
    details = {'company_name': settings.COMPANY_NAME,
               'slogan': settings.COMPANY_SLOGAN,
               'contacts': settings.COMPANY_CONTACTS}
    return Response(details)


###___Pagination___###
class RunsPagination(PageNumberPagination):
    page_size_query_param = 'size'


class UserPagination(PageNumberPagination):
    page_size_query_param = 'size'


###___Views___###
class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']
    pagination_class = RunsPagination



class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['date_joined']
    pagination_class = UserPagination

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
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            run.status = 'in_progress'
            run.save()
            return Response(run.status, status=status.HTTP_200_OK)



class StopRunView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status == 'init' or run.status == 'finished':
            return Response( status=status.HTTP_400_BAD_REQUEST)
        else:
            run.status = 'finished'
            run.save()
            return Response(run.status, status=status.HTTP_200_OK)


class AthleteInfoView(APIView):
    def get(self, request, user_id):
        # Проверяем существование юзера, получаем объект
        user_obj = get_object_or_404(User, id=user_id)

        # Обращаемся через объект user_obj
        athlete, _ = AthleteInfo.objects.get_or_create(
            user_id=user_obj,
            defaults={'weight': 0, 'goal': ''}
        )

        serializer = AthleteInfoSerializer(athlete)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user_obj = get_object_or_404(User, id=user_id)

        # Сначала находим или создаем объект
        athlete, _ = AthleteInfo.objects.get_or_create(
            user_id=user_obj,
            defaults={'weight': 0, 'goals': ''}
        )

        # Валидируем данные через сериализатор
        serializer = AthleteInfoSerializer(athlete, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Возвращаем 201 по условию задачи
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)