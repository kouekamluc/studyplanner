from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import get_study_time_per_course, get_task_completion_rate, get_productivity_trend, get_course_progress,get_dashboard_summary
from django.utils.dateparse import parse_date

class StudyTimePerCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = parse_date(request.query_params.get('start_date'))
        end_date = parse_date(request.query_params.get('end_date'))
        data = get_study_time_per_course(request.user, start_date, end_date)
        return Response(data)

class TaskCompletionRateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = parse_date(request.query_params.get('start_date'))
        end_date = parse_date(request.query_params.get('end_date'))
        data = get_task_completion_rate(request.user, start_date, end_date)
        return Response(data)

class ProductivityTrendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = parse_date(request.query_params.get('start_date'))
        end_date = parse_date(request.query_params.get('end_date'))
        data = get_productivity_trend(request.user, start_date, end_date)
        return Response(data)

class CourseProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_course_progress(request.user)
        return Response(data)
    

class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_dashboard_summary(request.user)
        return Response(data)