from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, views, response, status
from .serializers import UserSerializer, AnnouncementSerializer, SubjectSerializer, AttendanceSerializer, ResultsSerializer, ChangePasswordSerializer, UserStatusSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Announcement, Subject, Attendance, Results

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class StudentUserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class AnnouncementCreate(generics.ListCreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer): #Function to override the default creation process.
        if serializer.is_valid():
            serializer.save(author=self.request.user) # Automatically assigns the signed in user as the author of the post.
        else:
            print(serializer.errors)

class AnnouncementDelete(generics.DestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

class SubjectCreate(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

class AttendanceCreate(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    permission_classes = [IsAuthenticated]

class AttendanceListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Attendance.objects.filter(student=user) # Only returns the attendance list of the signed in user

class ResultsCreate(generics.ListCreateAPIView):
    serializer_class = ResultsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Results.objects.all()

class ResultsListView(generics.ListAPIView):
    serializer_class = ResultsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Results.objects.filter(student=user)
    
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

class UserStatusView(generics.RetrieveAPIView):
    serializer_class = UserStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user