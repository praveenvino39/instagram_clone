from django.views.generic.base import View
from posts.views import delete_post, get_post, get_user_post, create_post, like_post, post_comment, unlike_post, update_comment, update_post
from django.urls import path


urlpatterns = [
    path('create-post/', view=create_post, name="create_post"),
    path('<int:post_id>', view=get_post, name="get_post"),
    path('update-post/<int:post_id>', view=update_post, name="update_post"),
    path('delete-post/<int:post_id>', view=delete_post, name="delete_post"),
    path('like-post/<int:post_id>', view=like_post, name="like_post"),
    path('unlike-post/<int:post_id>', view=unlike_post, name="unlike_post"),
    path('post-comment', view=post_comment, name="post_comment"),
    path('update-comment/<int:post_id>',
         view=update_comment, name="update_comment"),
    path('/<str:username>', view=get_user_post, name="get_user_post"),
]
