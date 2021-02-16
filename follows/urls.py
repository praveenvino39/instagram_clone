from django.urls import path
from .views import follow_user, get_follower_list, get_following_list, unfollow_user


urlpatterns = [
    path('<str:follow_username>', view=follow_user, name="follow_user"),
    path('<str:username>/followers/',
         view=get_follower_list, name="get_follower_list"),
    path('<str:username>/followings/',
         view=get_following_list, name="get_following_list"),
    path('unfollow/<str:unfollow_username>',
         view=unfollow_user, name="unfollow_user")
]
