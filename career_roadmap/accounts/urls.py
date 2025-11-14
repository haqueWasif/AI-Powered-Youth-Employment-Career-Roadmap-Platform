from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    LogoutView, 
    CurrentUserView,
    ProfileDetailView,
    AddSkillView,
    RemoveSkillView
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', CurrentUserView.as_view(), name='current-user'),
    
    # Profile endpoints
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/add-skill/', AddSkillView.as_view(), name='add-skill'),
    path('profile/remove-skill/', RemoveSkillView.as_view(), name='remove-skill'),
]
