from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.generics import get_object_or_404
from django.http import Http404, HttpResponse
from .models import Post
from user.models import User


class PostAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data) # todo add likes counts and posts counts
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        snippets = Post.objects.all()
        serializer = PostSerializer(snippets, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = get_object_or_404(Post.objects.all(), pk=pk)
        serializer = PostSerializer(instance=post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post = get_object_or_404(Post.objects.all(), pk=pk)
        post.delete()
        return Response(status=status.HTTP_200_OK)

    class Meta:
        model = Post
        fields = ['__all__']


class PostLikesAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        model = get_object_or_404(Post, pk=pk)
        data = {"like": model.like + 1}
        serializer = PostSerializer(model, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    class Meta:
        model = Post
        fields = ['__all__']


class PostUnlikesAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        model = get_object_or_404(Post, pk=pk)
        data = {"unlike": model.unlike + 1}
        serializer = PostSerializer(model, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    class Meta:
        model = Post
        fields = ['__all__']
