
from django.db.models import Avg, Sum, F
from django.utils import timezone

from planner.models import Course, Task, StudySession

def get_study_time_per_course(user, start_date=None, end_date=None):
    query = StudySession.objects.filter(user=user)
    if start_date:
        query = query.filter(start_time__gte=start_date)
    if end_date:
        query = query.filter(end_time__lte=end_date)
    
    return query.values('course__name').annotate(
        total_duration=Sum(F('end_time') - F('start_time'))
    )


def get_productivity_trend(user, start_date=None, end_date=None):
    query = StudySession.objects.filter(user=user)
    if start_date:
        query = query.filter(start_time__gte=start_date)
    if end_date:
        query = query.filter(end_time__lte=end_date)
    
    return query.values('start_time__date').annotate(
        avg_productivity=Avg('productivity_rating')
    ).order_by('start_time__date')

def get_course_progress(user):
    courses = Course.objects.filter(user=user)
    progress_data = []
    
    for course in courses:
        total_tasks = Task.objects.filter(course=course).count()
        completed_tasks = Task.objects.filter(course=course, completed=True).count()
        progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        progress_data.append({
            'course_name': course.name,
            'progress': progress
        })
    
    return progress_data




def get_task_completion_rate(user, start_date=None, end_date=None):
    query = Task.objects.filter(user=user)
    if start_date:
        query = query.filter(due_date__gte=start_date)
    if end_date:
        query = query.filter(due_date__lte=end_date)
    
    total_tasks = query.count()
    completed_tasks = query.filter(completed=True).count()
    
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': (completed_tasks / total_tasks) if total_tasks > 0 else 0
    }



def get_dashboard_summary(user):
    today = timezone.now().date()
    last_30_days = today - timezone.timedelta(days=30)
    
    return {
        'total_study_time': StudySession.objects.filter(user=user, start_time__gte=last_30_days).aggregate(
            total_time=Sum(F('end_time') - F('start_time'))
        )['total_time'],
        'courses_in_progress': Course.objects.filter(user=user, end_date__gte=today).count(),
        'tasks_due_soon': Task.objects.filter(user=user, due_date__gte=today, due_date__lte=today + timezone.timedelta(days=7), completed=False).count(),
        'recent_completion_rate': get_task_completion_rate(user, start_date=last_30_days)['completion_rate']
    }