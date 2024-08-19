
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CourseViewSet,FileViewSet, 
                    UserViewSet,TaskViewSet, StudySessionViewSet, 
                    LearningStyleViewSet
                    ,PomodoroSessionViewSet
                    )

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'users', UserViewSet, basename='user')
router.register(r'files', FileViewSet, basename='file')

router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'study-sessions', StudySessionViewSet, basename='studysession')
router.register(r'learning-styles', LearningStyleViewSet, basename='learningstyle')
router.register(r'pomodoro-sessions', PomodoroSessionViewSet, basename='pomodorosession')

urlpatterns = [
    path('', include(router.urls)),

]