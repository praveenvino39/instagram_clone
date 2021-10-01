import asyncio
import json
from django.db.models.fields.json import JSONExact
from rest_framework import status
from rest_framework.utils.serializer_helpers import JSONBoundField
from users.serializers import ProfileSerializer, UserSerializer
from users.models import Profile
from django.http.response import Http404
from posts.serializers import PostSerializer
import websockets
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from .models import Post
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.response import Response
import random
# Create your views here.


@api_view(['GET'])
def get_user_post(request, username):
    print(username)
    user = get_object_or_404(User, username=username)
    post = Post.objects.filter(user=user.id)
    post = PostSerializer(post, many=True)
    return Response(post.data)


@api_view(['POST'])
def create_post(request):
    if request.user.is_authenticated:
        post = Post(
            user=request.user,
            video_url=request.data.get("post_url"),
            post_image=request.data.get("image"),
            is_video=request.data.get("is_video"),
            caption=request.data.get("caption")
        )
        post.save()
        post = PostSerializer(post, many=False)
        return Response(post.data)
    else:
        return Response({"message": "Authentication details not provided"}, status=HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post = PostSerializer(post, many=False)
    return Response({"data": post.data, "likes_count": len(post.data["likes"])})


@api_view(['PUT'])
def update_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
        if post.user == request.user:
            if request.data.get('caption'):
                post.caption = request.data.get('caption')
                post.save()
                post = PostSerializer(post, many=False)
                return Response(post.data)
            else:
                return Response({"caption": "this field is required"})
        else:
            return Response("You dont\'t have permission to update this post")
    else:
        return Response("Authentication credentials not provided")



@api_view(['DELETE'])
def delete_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
        if post.user == request.user:
            post.delete(),
            post = PostSerializer(post, many=False)
            return Response(post.data)
        else:
            return Response("You dont\'t have permission to update this post")
    else:
        return Response("Authentication credentials not provided")


@api_view(['GET'])
def like_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
        if any(x["username"] == request.user.username for x in post.likes):
            return Response({"error": "Post already liked"})
        else:
            post.likes.append(
                {"username": request.user.username, "id": request.user.id})
            post.save()
            post = PostSerializer(post, many=False)
            return Response({"data": post.data, "likes_count": len(post.data["likes"])}, status=HTTP_200_OK)

    else:
        return Response({"error": "Authentication credentials not provided"}, status=HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def unlike_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
        if any(x["username"] == request.user.username for x in post.likes):
            post.likes.remove(
                {"username": request.user.username, "id": request.user.id})
            post.save()
            post = PostSerializer(post, many=False)
            return Response({"data": post.data, "likes_count": len(post.data["likes"])}, status=HTTP_200_OK)
        else:
            return Response({"error": "Post already unliked"})

    else:
        return Response({"error": "Authentication credentials not provided"}, status=HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def post_comment(request):
    if request.user.is_authenticated:
        if request.data.get("comment") != None:
            post = get_object_or_404(Post, pk=request.data.get("post_id"))
            post.comments.append(
                {"comment_id": random.randint(1, 100000), "username": request.user.username, "comment": request.data.get("comment"), "reply_to": request.data.get("parent_comment_id    ")})
            post.save()
            post = PostSerializer(post, many=False)
            return Response({"data": post.data, "comments_count": len(post.data["comments"])})
        else:
            return Response({"comment": "This is field is required."}, status=HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Authentication credential not provided"}, status=HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def update_comment(request, post_id):
    if request.user.is_authenticated:
        if request.data.get("comment_id") != None and request.data.get("comment") != None:
            post = get_object_or_404(Post, pk=post_id)
            update_comment = {}
            print(post.comments[1])
            for comment in post.comments:
                if comment["comment_id"] == int(request.data.get("comment_id")):
                    update_comment = comment
                    break
            if update_comment["comment_id"] == None:
                return Response({"error": "Comment not found"}, status=HTTP_404_NOT_FOUND)
            else:
                if update_comment["username"] == request.user.username:
                    update_comment["comment"] = request.data.get("comment")
                    post.save()
                    post = PostSerializer(post, many=False)
                    return Response(post.data)
                else:
                    return Response({"error": "Not authorized to edit this comment"}, status=HTTP_401_UNAUTHORIZED)
        else:
            return Response({"comment_id": "This field is required", "comment": "This field is required."}, status=HTTP_400_BAD_REQUEST)

    else:
        return Response({"error": "Authentication credential not provided"}, status=HTTP_401_UNAUTHORIZED)
