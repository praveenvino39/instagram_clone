from posts.serializers import PostSerializer
from posts.models import Post
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from users.models import Profile
from django.shortcuts import get_object_or_404
from users.serializers import ProfileSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


@api_view(['POST'])
def registration(request):
    user = User.objects.create(username=request.data.get(
        "username"), password=make_password(request.data.get("password")), email="")
    user.save()
    user_profile = Profile(user=user)
    user_profile.save()
    user_profile = ProfileSerializer(user_profile, many=False)
    return Response(user_profile.data, status=HTTP_201_CREATED)


@api_view(['PUT'])
def update_password(request):
    if request.user.is_authenticated:
        if request.data.get("password") != None and request.data.get("new_password") != None:
            user = get_object_or_404(User, username=request.user.username)
            if user.check_password(request.data.get("password")):
                user.set_password(request.data.get("new_password"))
                user.save()
                user = UserSerializer(user, many=False)
                return Response(user.data)
            else:
                return Response({"error": "Username or password invalid"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"password": "This field is required", "new_password": "This field is required"}, status=HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Authentication details not provided"}, status=HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def update_username(request):
    if request.user.is_authenticated:
        if request.data.get("password") != None and request.data.get("username") != None:
            user = get_object_or_404(User, username=request.user.username)
            if user.check_password(request.data.get("password")):
                user.username = request.data.get("username")
                user.save()
                user = UserSerializer(user, many=False)
                return Response(user.data)
            else:
                return Response({"error": "Username or password invalid"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"username": "This field is required", "password": "This field is required"}, status=HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Authentication details not provided"}, status=HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def update_profile(request):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(Profile, user=request.user)
        user_profile.bio = request.data.get("bio")
        user_profile.website = request.data.get("website")
        user_profile.save()
        user_profile = ProfileSerializer(user_profile, many=False)
        return Response(user_profile.data)
    else:
        return Response({"error": "Authentication details not provided"}, status=HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = Profile.objects.filter(user=user.id).first()
    follower_count = len(user_profile.followers)
    following_count = len(user_profile.following)
    posts = Post.objects.filter(user=user)
    posts = PostSerializer(posts, many=True)
    user_profile = ProfileSerializer(user_profile, many=False)
    return Response({"data": user_profile.data, "posts": posts.data, "post_count": len(posts.data), "follower_count": follower_count, "following_count": following_count}, status=HTTP_200_OK)
