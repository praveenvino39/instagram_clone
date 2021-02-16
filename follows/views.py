from users.serializers import ProfileSerializer, UserSerializer
from django.contrib.auth.models import User
from posts.models import Post
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.serializers import PostSerializer
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from users.models import Profile
# Create your views here.


@api_view(['GET'])
def follow_user(request, follow_username):
    follow_user = get_object_or_404(User, username=follow_username)
    if request.user.is_authenticated and (request.user != follow_user):
        follow_user_profile = Profile.objects.filter(
            user=follow_user).first()
        if any(x["username"] == request.user.username for x in follow_user_profile.followers):
            return Response({"message": "User already followed"}, status=HTTP_200_OK)
        else:
            # Adding requesting user to the follower list
            follow_user_profile.followers.append(
                {"username": request.user.username})
            follow_user_profile.save()

            # Adding followed user to the following list
            request_user_profile = get_object_or_404(
                Profile, user=request.user)
            request_user_profile.following.append(
                {"username": follow_user.username})
            request_user_profile.save()
            request_user_profile = ProfileSerializer(
                request_user_profile, many=False)
            return Response(request_user_profile.data, status=HTTP_200_OK)
    else:
        return Response({"error": "Authentication credential not found"}, status=HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def unfollow_user(request, unfollow_username):
    unfollow_user = User.objects.filter(username=unfollow_username).first()
    if request.user.is_authenticated and (request.user != unfollow_user):
        unfollow_user_profile = Profile.objects.filter(
            user=unfollow_user).first()
        if any(x["username"] == request.user.username for x in unfollow_user_profile.followers):
            # Removing requested user from user followers list
            unfollow_user_profile.followers.remove(
                {"username": request.user.username})
            unfollow_user_profile.save()

            # Removing unfollow user from requested user following list
            request_user_profile = get_object_or_404(
                Profile, user=request.user)
            request_user_profile.following.remove(
                {"username": unfollow_user.username})
            unfollow_user_profile = ProfileSerializer(
                unfollow_user_profile, many=False)
            request_user_profile.save()
            request_user_profile = ProfileSerializer(
                request_user_profile, many=False)
            return Response(request_user_profile.data, status=HTTP_200_OK)
        else:
            return Response({"message": "User not followed"}, status=HTTP_404_NOT_FOUND)

    else:
        return Response({"error": "Authentication credential not found"}, status=HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def get_follower_list(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Profile, user=user)
    user_profile = ProfileSerializer(user_profile, many=False)
    return Response({"followers": user_profile.data["followers"]}, status=HTTP_200_OK)


@api_view(["GET"])
def get_following_list(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Profile, user=user)
    user_profile = ProfileSerializer(user_profile, many=False)
    return Response({"followings": user_profile.data["following"]}, status=HTTP_200_OK)
