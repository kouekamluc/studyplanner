from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
# Create your views here.
from rest_framework import viewsets, status,filters
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Course, File, Tag,Task, StudySession, LearningStyle,PomodoroSession
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import (FileSerializer,TagSerializer, 
                          CourseSerializer,
                          UserRegistrationSerializer,
                          PomodoroSessionSerializer,
                          TaskSerializer,UserSerializer, 
                          StudySessionSerializer, LearningStyleSerializer)
import logging
from .filters import CourseFilter, TaskFilter, StudySessionFilter


logger = logging.getLogger(__name__)






class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                logger.info(f"New user registered: {serializer.validated_data['username']}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error during user registration: {str(e)}")
                return Response({"error": "Registration failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.warning(f"Invalid registration attempt: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
def get_queryset(self):
    return Tag.objects.filter(user=self.request.user)

def perform_create(self, serializer):
    serializer.save(user=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = CourseFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description', 'tags__name']



    def get_queryset(self):
        return Course.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
    def upload_file(self, request, pk=None):
        course = self.get_object()
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save(user=request.user, course=course)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['get'])
    def add_tag(self, request, pk=None):
        course = self.get_object()
        tag_name = request.data.get('name')
        if  tag_name:
            tag, _ = Tag.objects.get_or_create(name=tag_name, user=request.user)
            course.tags.add(tag)
            return Response({'status': 'tag added'})
        return Response({'status': 'error', 'message': 'Tag name is required'}, status=400)

    @action(detail=True, methods=['get'])
    def remove_tag(self, request, pk=None):
        course = self.get_object()
        tag_name = request.data.get('tag')
        if  tag_name:
            tag = Tag.objects.filter(name=tag_name, user=request.user).first()
            if tag:
                course.tags.remove(tag)
                return Response({'status': 'tag removed'})
            return Response({'status': 'error', 'message': 'Tag not found'}, status=404)
        return Response({'status': 'error', 'message': 'Tag name is required'}, status=400)
       

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description', 'tags__name']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
    def upload_file(self, request, pk=None):
        task = self.get_object()
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save(user=request.user, task=task)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['post'])
    def add_tag(self, request, pk=None):
        task = self.get_object()
        tag_name = request.data.get('tag')
        if tag_name:
            tag, _ = Tag.objects.get_or_create(name=tag_name, user=request.user)
            task.tags.add(tag)
            return Response({'status': 'tag added'})
        return Response({'status': 'error', 'message': 'Tag name is required'}, status=400)

    @action(detail=True, methods=['post'])
    def remove_tag(self, request, pk=None):
        task = self.get_object()
        tag_name = request.data.get('tag')
        if tag_name:
            tag = Tag.objects.filter(name=tag_name, user=request.user).first()
            if tag:
                task.tags.remove(tag)
                return Response({'status': 'tag removed'})
            return Response({'status': 'error', 'message': 'Tag not found'}, status=404)
        return Response({'status': 'error', 'message': 'Tag name is required'}, status=400)
    
    
class StudySessionViewSet(viewsets.ModelViewSet):
    serializer_class = StudySessionSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = StudySessionFilter

    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LearningStyleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LearningStyleSerializer

    def get_queryset(self):
        return LearningStyle.objects.filter(user=self.request.user)
    
    

class PomodoroSessionViewSet(viewsets.ModelViewSet):
    serializer_class = PomodoroSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PomodoroSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        pomodoro = self.get_object()
        if pomodoro.start_time is None:
            pomodoro.start_time = timezone.now()
            pomodoro.save()
            return Response({'status': 'Pomodoro session started'})
        return Response({'status': 'Pomodoro session already started'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        pomodoro = self.get_object()
        if pomodoro.end_time is None:
            pomodoro.end_time = timezone.now()
            pomodoro.completed = True
            pomodoro.save()
            return Response({'status': 'Pomodoro session completed'})
        return Response({'status': 'Pomodoro session already completed'}, status=status.HTTP_400_BAD_REQUEST)