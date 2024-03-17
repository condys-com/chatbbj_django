"""
URL configuration for chatbbj_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from chatbbj_app import views
from chatbbj_app.views import CustomAuthToken, UserDetailView, UserRegistration, ChatHistoryView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/download/', views.download_file),
    path('api/login/', CustomAuthToken.as_view()),
    path('api/user/', UserDetailView.as_view()),
    path('api/register/', UserRegistration.as_view()),
    path('api/chathistory/', ChatHistoryView.as_view()),
    path('api/messages/<str:username>/', views.get_chat_history, name='get_chat_history'),
]
