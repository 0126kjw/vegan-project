from django.db import models
from django.contrib.sessions.models import Session



class Posts(models.Model):
    ID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255, blank=True, null=False)
    Content = models.TextField(null=False)
    Thumbnail = models.ImageField(upload_to="./thumbnail", null=True)
    Type = models.CharField(max_length=40, blank=True, null=False)
    Hashtag = models.CharField(max_length=255, blank=True, null=True)
    User = models.ForeignKey(
        "accounts.user", to_field="email", on_delete=models.CASCADE)
    Groups = models.IntegerField(null=False)
    RestaurantsId = models.IntegerField(null=True)
    Address = models.CharField(max_length=255, blank=True, null=True)
    CreationTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Title


class Comments(models.Model):
    CommentId = models.AutoField(primary_key=True)
    User = models.ForeignKey(
        "accounts.user", to_field="email", on_delete=models.CASCADE)
    PostId = models.ForeignKey(Posts, on_delete=models.CASCADE)
    Comment = models.TextField(null=False)
    CreationTime = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.CommentId


class Like(models.Model):
    PostId = models.ForeignKey(Posts, on_delete=models.CASCADE)
    User = models.ForeignKey(
        "accounts.user", to_field="email", on_delete=models.CASCADE)
    Like = models.BooleanField(default=False, null=False)


class Image(models.Model):
    User = models.ForeignKey(
        "accounts.user", to_field="email", on_delete=models.CASCADE)
    Image = models.ImageField(upload_to="./post", null=False)
    is_editing = models.BooleanField(default=True, null=False)
    PostId = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)
    CreationTime = models.DateTimeField(auto_now_add=True)
    EditId = models.ForeignKey(
        Session, on_delete=models.CASCADE, null=True)
