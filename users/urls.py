from users.views import registration, update_password, update_profile, update_username, user_detail, getToken, profile
from django.urls import path
from rest_framework import routers, views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('registration/', view=registration, name="registration"),
    path('profile/', view=profile, name="profile"),
    path('login/', view=getToken, name="login"),
    path('update-profile', view=update_profile, name="update_profile"),
    path('change-password', view=update_password, name="update_password"),
    path('change-username', view=update_username, name="update_username"),
    path('<str:username>', view=user_detail, name="user_detail")
]
