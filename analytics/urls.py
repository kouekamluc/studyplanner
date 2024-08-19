from django.urls import path
from .views import DashboardSummaryView,StudyTimePerCourseView, TaskCompletionRateView, ProductivityTrendView, CourseProgressView

urlpatterns = [
    path('study-time-per-course/', StudyTimePerCourseView.as_view(), name='study-time-per-course'),
    path('task-completion-rate/', TaskCompletionRateView.as_view(), name='task-completion-rate'),
    path('productivity-trend/', ProductivityTrendView.as_view(), name='productivity-trend'),
    path('course-progress/', CourseProgressView.as_view(), name='course-progress'),
    path('dashboard-summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
]