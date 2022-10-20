from rest_framework import serializers
from .models import Posts, Comments, Like, Image


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('ID', 'User', 'Title', 'Content', 'Thumbnail', 'Type',
                  'Hashtag', "CreationTime", 'Groups', 'RestaurantsId', 'Address')


class PostUpdataNoThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('ID', 'User', 'Title', 'Content',  'Type',
                  'Hashtag', "CreationTime", 'Groups', 'RestaurantsId', 'Address')


class CommentsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('CommentId', 'User', 'PostId', 'Comment', "CreationTime")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('PostId', 'User', 'Like')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('User', 'Image', 'EditId')


class ImageSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('User', 'Image', 'EditId', 'is_editing', 'PostId')
