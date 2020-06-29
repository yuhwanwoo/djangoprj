from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('delete/', views.delete, name="delete"),
    path('update/', views.update, name="update"),
    path('password/', views.password, name="password"),
    path('follow/<int:user_pk>/', views.follow, name="follow"),
    path('<str:username>/', views.profile, name="profile"), # 문자열 하나만 받을 친구는 밑에 둬야한다.(오류생김)
]