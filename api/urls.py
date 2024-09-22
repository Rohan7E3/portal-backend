from django.urls import path
from . import views

urlpatterns = [
    path("announcements/", views.AnnouncementCreate.as_view(), name="announcements"),
    path("announcements/delete/<int:pk>/", views.AnnouncementDelete.as_view(), name="delete-announcement"),
    path("current-user/", views.CurrentUserView.as_view(), name="current-user"),    
    path("subjects/", views.SubjectListView.as_view(), name="subjects"),
    path("subjects/create/", views.SubjectCreate.as_view(), name="subject-create"),
    path("attendance/create/", views.AttendanceCreate.as_view(), name="attendance-create"),
    path("attendance/", views.AttendanceListView.as_view(), name="attendance"),
    path("results/", views.ResultsListView.as_view(), name="results"),
    path("results/create/", views.ResultsCreate.as_view(), name="create-result"),
    path("change-password/<int:pk>/", views.ChangePasswordView.as_view(), name="auth-change-password"),
    path("user-status/", views.UserStatusView.as_view(), name="user-status"),
    path("user/delete/<int:pk>/", views.DeleteUserView.as_view(), name="user-delete"),
]