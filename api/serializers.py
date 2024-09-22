from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Announcement, Subject, Attendance, Results

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class AnnouncementSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(source='author.first_name', read_only = True)
    author_last_name = serializers.CharField(source='author.last_name', read_only = True)

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'author', 'author_first_name', 'author_last_name', 'created_at']
        extra_kwargs = {'author': {'read_only': True}}

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['code', 'name']

class AttendanceSerializer(serializers.ModelSerializer):
    subject_name = serializers.StringRelatedField(source='subject_code.name')
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=False))

    class Meta:
        model = Attendance
        fields = ['id', 'date', 'subject_code', 'subject_name', 'student', 'status']

class ResultsSerializer(serializers.ModelSerializer):
    subject_name = serializers.StringRelatedField(source='subject_code.name')
    sub = serializers.StringRelatedField(source='subject_code.code')
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=False))

    class Meta:
        model = Results
        fields = ['id', 'date', 'subject_code', 'subject_name', 'sub', 'student', 'score', 'max_score', 'status']

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User 
        fields = ['old_password', 'new_password']

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'old_password': 'Old password does not match'})
        return value
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
    
class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_staff', 'is_superuser']