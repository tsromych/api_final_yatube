from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Group, Post
from .mixins import CreateListViewSet
from .permissions import AuthorPermission
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет получения, обновления, изменения и удаления постов."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorPermission,)

    def perform_create(self, serializer):
        """Метод создания нового поста."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет получения данных групп пользователей."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AuthorPermission,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет получения, обновления, изменения и удаления комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorPermission,)

    def post_or_404(self):
        """Метод получения объекта поста."""
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Метод для выборки комментариев к конкретному посту."""
        return self.post_or_404().comments.all()

    def perform_create(self, serializer):
        """Метод создания нового комментария к посту."""
        serializer.save(author=self.request.user, post=self.post_or_404())


class FollowViewSet(CreateListViewSet):
    """Вьюсет получения, обновления, изменения, удаления и поиска подписок."""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('user__username', 'following__username',)

    def get_queryset(self):
        """Метод для выборки авторов, на которых подписан
        пользователь."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Метод создания новой подписки."""
        serializer.save(user=self.request.user)
