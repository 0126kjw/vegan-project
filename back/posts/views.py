import re
import jwt
from rest_framework import status
from django.conf import settings
from django.db.models import Count, Subquery, OuterRef
from .serializers import PostSerializer, CommentsItemSerializer, LikeSerializer, ImageSerializer, PostUpdataNoThumbnailSerializer
from accounts.models import User
from .models import Image, Posts, Like, Comments
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.db.models import Q
import sys
import os
import re
from urllib import parse
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class PostAllGetAPI(APIView):
    model = Posts

    def get(self, request):
        items = Posts.objects
        Page = 1
        Sort = "CreationTime"
        keys = request.GET.keys()

        q = Q()
        if "ID" in keys:
            q &= Q(ID=request.GET["ID"])

        if "Groups" in keys:
            q &= Q(Groups__in=request.GET["Groups"])

        if "Content" in keys:
            q &= Q(Content__contains=request.GET["Content"])

        if "Address" in keys:
            q &= Q(Address__contains=request.GET["Address"])

        if "Type" in keys:
            q &= Q(Type__contains=request.GET["Type"])

        if "Hashtag" in keys:
            q &= Q(Hashtag__contains=request.GET["Hashtag"])

        if "Title" in keys:
            q &= Q(Title__contains=request.GET["Title"])

        if "User" in keys:
            q &= Q(User=request.GET["User"])

        if "Sort" in keys:
            Sort = request.GET["Sort"]
        if "Page" in keys:
            Page = request.GET["Page"]

        items = items.filter(q).values("ID", "Groups", "Type", "Title", "Thumbnail",
                                       "CreationTime", "User").order_by(Sort)
        paginator = Paginator(items, 12)

        responseData = list(paginator.get_page(Page).object_list)

        test_data_p = [responseData[i]["ID"] for i in range(len(responseData))]
        test_data_set = Like.objects.values(
            "PostId_id").annotate(Count('Like')).values("PostId_id", "Like__count").filter(PostId_id__in=test_data_p)

        test_data_l = [test_data_set[i]["PostId_id"]
                       for i in range(len(test_data_set))]

        for i in range(len(test_data_p)):
            if test_data_p[i] in test_data_l:
                index_l = test_data_l.index(test_data_p[i])
                responseData[i]["Likes"] = test_data_set[index_l]["Like__count"]
            else:
                responseData[i]["Likes"] = 0

        responseData_Page = {"list": responseData,
                             "page": {"num_pages": paginator.num_pages, "now": Page}}

        return Response(responseData_Page)

    def post(self, request):
        img_re = re.compile(r'(img\/)(.+?)"')
        user = request.user
        data = request.data.copy()
        data["User"] = user
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            img_list_set = img_re.findall(data["Content"])
            img_list = []
            for i in range(len(img_list_set)):
                img_list.append(parse.unquote(img_list_set[i][1]))
            if img_list:
                # items = Image.objects.filter(Image=img_list)
                # print(items)
                items = Image.objects.filter(
                    Image__in=img_list)
                items.update(is_editing=False,
                             PostId_id=serializer.data["ID"], EditId=None)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostGetAPI(APIView):
    def get(self, request, ID):
        item = Posts.objects.get(ID=ID)
        responseData = PostSerializer(item)

        return (Response(responseData.data))

    def put(self, request, ID):
        item = Posts.objects.get(ID=ID)
        user = request.user
        if item.User != user:
            return Response("본인 게시글이 아닙니다", status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        data["User"] = user
        if type(data["Thumbnail"]) is str:
            del data["Thumbnail"]
            serializer = PostUpdataNoThumbnailSerializer(item, data=data)
        else:
            serializer = PostSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ID):
        item = Posts.objects.get(ID=ID)
        if item.User != request.user:
            return Response("본인 게시글이 아닙니다", status=status.HTTP_400_BAD_REQUEST)
        item.delete()
        return Response("deleted:"+str(ID))


class PostCommentsAPI(APIView):

    def get(self, request, ID):
        item = Comments.objects.filter(PostId=ID).values()

        return Response(item)

    def post(self, request, ID):
        data = request.data.copy()
        data["User"] = request.user
        data["PostId"] = ID
        serializer = CommentsItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ID, ):
        item = Comments.objects.get(CommentId=request.GET["CommentId"])
        if item.User != request.user:
            return Response("본인 게시글이 아닙니다")
        item.delete()
        return Response("deleted:"+str(ID))


class PostLikeAPI(APIView):
    def get(self, request, ID):
        return Response(Like.objects.filter(PostId=ID).count())

    def post(self, request, ID):
        try:
            item = Like.objects.get(PostId=ID, User=request.user)
            item.delete()
            return Response(Like.objects.filter(PostId=ID).count())
        except Like.DoesNotExist:
            serializer = LikeSerializer(
                data={"PostId": ID, "User": request.user, "Like": True})
            if serializer.is_valid():
                serializer.save()
                return Response(Like.objects.filter(PostId=ID).count())
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageApi(APIView):
    def post(self, request):
        data = request.data.copy()
        data["User"] = request.user
        data["EditId"] = request.COOKIES.get("sessionid")
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
