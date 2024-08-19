
from rest_framework import serializers
from .models import Course, Task, StudySession, LearningStyle, UserProfile , Tag,File,PomodoroSession

from django.contrib.auth.models import User



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user




class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'name', 'uploaded_at', 'course', 'task']
        read_only_fields = ['uploaded_at']



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'birth_date', 'time_zone', 'preferred_study_time', 'daily_study_goal']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.bio = profile_data.get('bio', profile.bio)
        profile.birth_date = profile_data.get('birth_date', profile.birth_date)
        profile.time_zone = profile_data.get('time_zone', profile.time_zone)
        profile.preferred_study_time = profile_data.get('preferred_study_time', profile.preferred_study_time)
        profile.daily_study_goal = profile_data.get('daily_study_goal', profile.daily_study_goal)
        profile.save()

        return instance


class CourseSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    files = FileSerializer(many=True, read_only=True)


    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'difficulty_level', 'color', 'tags', 'files']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        course = Course.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_data['name'], user=course.user)
            course.tags.add(tag)
        return course


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    files = FileSerializer(many=True, read_only=True)


    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'estimated_time', 'priority', 'completed', 'reminder', 'tags', 'files']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_data['name'], user=task.user)
            task.tags.add(tag)
        return task
    
class StudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySession
        fields = '__all__'

class LearningStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningStyle
        fields = '__all__'
        
    

class PomodoroSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PomodoroSession
        fields = ['id', 'task', 'start_time', 'end_time', 'duration', 'completed']
        read_only_fields = ['start_time', 'end_time', 'completed']