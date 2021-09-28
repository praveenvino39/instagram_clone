from posts.serializers import PostSerializer
from posts.models import Post
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from users.models import Profile
from django.shortcuts import get_object_or_404
from users.serializers import ProfileSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import  Token
from django.db import IntegrityError

@api_view(['POST'])
def registration(request):
    if request.data.get("username") and request.data.get("password"):
        try:
            user = User.objects.create(username=request.data.get(
                "username"), password=make_password(request.data.get("password")), email="")
            user.save()
            user_profile = Profile(user=user)
            user_profile.save()
            user_profile = ProfileSerializer(user_profile, many=False)
            user = UserSerializer(user,many=False)
            return Response({"data": {"user_profile":user_profile.data, "user_data": user.data}, "status": True, "message": "User created successfully"}, status=HTTP_201_CREATED)
        except IntegrityError:
            return Response({"message": "Username already exist","data": {}, "status": False}, status = HTTP_200_OK)

    else:
        return Response({"message": "Username or Password is empty","data": {}, "status":False}, status = HTTP_200_OK)


@api_view(['POST'])
def getToken(request):
    if request.data.get("username") and request.data.get("password"):
        user = get_object_or_404(User, username=request.data.get("username"))
        token, created = Token.objects.get_or_create(user=user)
        user_profile = get_object_or_404(Profile, user=user)
        user_profile = ProfileSerializer(user_profile, many=False)
        user = UserSerializer(user,many=False)
        return Response({"data": {"user_profile":user_profile.data, "user_data": user.data, "token": token.key}, "status": True, "message": "Loggin successfully"}, status=HTTP_201_CREATED)


    else:
        return Response({"message": "Username or Password is empty","data": {}, "status":False}, status = HTTP_200_OK)




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
            try:
                user = get_object_or_404(User, username=request.user.username)
                if user.check_password(request.data.get("password")):
                    user.username = request.data.get("username")
                    user.save()
                    user = UserSerializer(user, many=False)
                    return Response(user.data, status=HTTP_200_OK)
            except IntegrityError:
                return Response({"message": "Username not available","data": {}},status=HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Username or password invalid"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"username": "This field is required", "password": "This field is required"}, status=HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Authentication details not provided"}, status=HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def update_profile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        if user:
            user_profile = get_object_or_404(Profile, user=request.user)
            user_profile.profile_picture = request.FILES.get("profile_picture") if request.FILES.get("profile_picture") else user_profile.profile_picture
            user_profile.bio = request.data.get("bio") if request.data.get("bio") else user_profile.bio
            user_profile.website = request.data.get("website") if request.data.get("website") else user_profile.website
            user_profile.is_private = request.data.get("is_private") if request.data.get("is_private") else user_profile.is_private
            user_profile.save()
            user.first_name = request.data.get("first_name") if request.data.get("first_name") else user.first_name
            user.last_name = request.data.get("last_name") if request.data.get("last_name") else user.last_name
            user.email = request.data.get("email") if request.data.get("email") else user.email
            user.save()
            user_profile = ProfileSerializer(user_profile, many=False)
            return Response(user_profile.data)
        else:
            return Response({"message": "Account not found"}, status=HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "Authentication details not provided"}, status=HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = Profile.objects.filter(user=user.id).first()
    if user_profile.is_private:
        if request.user.is_authenticated:
            is_followed = False
            for item in user_profile.followers:
                if(item["id"] == request.user.id):
                    is_followed = True
            if is_followed:
                follower_count = len(user_profile.followers)
                following_count = len(user_profile.following)
                posts = Post.objects.filter(user=user)
                posts = PostSerializer(posts, many=True)
                user_profile = ProfileSerializer(user_profile, many=False)
                return Response({"data": user_profile.data, "posts": posts.data, "post_count": len(posts.data), "follower_count": follower_count, "following_count": following_count}, status=HTTP_200_OK)
            else:
                user = UserSerializer(user, many=False)
                return Response({"data": user.data})
        else:
            user = UserSerializer(user, many=False)
            return Response({"data": user.data})
    else:
        follower_count = len(user_profile.followers)
        following_count = len(user_profile.following)
        posts = Post.objects.filter(user=user)
        posts = PostSerializer(posts, many=True)
        user_profile = ProfileSerializer(user_profile, many=False)
        return Response({"data": user_profile.data, "posts": posts.data, "post_count": len(posts.data), "follower_count": follower_count, "following_count": following_count}, status=HTTP_200_OK)
