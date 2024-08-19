import django_filters
from .models import Course, Task, StudySession







class CourseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    tags = django_filters.CharFilter(field_name='tags__name', lookup_expr='iexact')

    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = Course
        fields = ['name', 'start_date', 'end_date', 'difficulty_level']

class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    tags = django_filters.CharFilter(field_name='tags__name', lookup_expr='iexact')

    due_date = django_filters.DateFromToRangeFilter()
    completed = django_filters.BooleanFilter()

    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority', 'completed']

class StudySessionFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFromToRangeFilter()
    course = django_filters.ModelChoiceFilter(queryset=Course.objects.all())

    class Meta:
        model = StudySession
        fields = ['start_time', 'course', 'productivity_rating']