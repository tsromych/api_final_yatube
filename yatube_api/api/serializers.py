from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор постов."""
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = "__all__"
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор групп."""
    class Meta:
        fields = "__all__"
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("post",)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""
    user = SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    following = SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )

    class Meta:
        fields = "__all__"
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=("user", "following"),
                message=("Подписка на этого автора уже оформлена."),
            )
        ]

    def validate_following(self, data):
        if self.context["request"].user == data:
            raise serializers.ValidationError(
                "Вы не можете подписаться на самого себя!"
            )
        return data
