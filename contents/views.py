from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import Profile
from django.contrib.auth.models import User
from posts.models import Post
from posts.serializers import PostSerializer
from users.serializers import ProfileSerializer, UserSerializer
from rest_framework import status
# Create your views here.


@api_view(['GET'])
def home(request):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(Profile, user=request.user)
        following_list = []
        for following in user_profile.following:
            following_list.append(following["username"])
        post_list = []
        for user in following_list:
            u = get_object_or_404(User, username=user)
            posts = Post.objects.filter(user=u)
            for post in posts:
                profile = get_object_or_404(Profile, user=post.user)
                user_profile = ProfileSerializer(profile, many=False)
                is_current_user_liked = False
                if any(x["id"] == request.user.id for x in post.likes):
                    is_current_user_liked = True
                post = PostSerializer(post, many=False)
                post_list.append(
                    {"post": post.data, "is_current_user_liked": is_current_user_liked, "profile": user_profile.data})
            post_list = sorted(
                post_list, key=lambda x: x["post"]["timestamp"], reverse=True)
        return Response(post_list, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Authentication credential not provided"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def search(request):
    if request.data.get("keyword"):
        post_list = []
        user_list = []
        posts = Post.objects.filter(
            caption__contains=request.data.get("keyword"))
        for post in posts:
            post = PostSerializer(post, many=False)
            post_list.append(post.data)
        post_list = sorted(
            post_list, key=lambda x: x["timestamp"], reverse=True)
        users = User.objects.filter(
            username__contains=request.data.get("keyword"))
        for user in users:
            user = UserSerializer(user, many=False)
            user_list.append(user.data)
        user_list = sorted(
            user_list, key=lambda x: x["last_login"], reverse=True)
        return Response({"posts": {"post_result": post_list, "result_length": len(post_list)}, "users": {"user_result": user_list, "result_length": len(user_list)}, }, status=status.HTTP_200_OK)
    else:
        return Response({"keyword": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)
