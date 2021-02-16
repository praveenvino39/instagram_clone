from .models import Post
from rest_framework.serializers import ModelSerializer
from users.serializers import UserSerializer


class PostSerializer(ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Post
        fields = '__all__'
