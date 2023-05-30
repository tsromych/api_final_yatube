from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Укажите название группы')
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
        help_text='Укажите слаг')
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание группы')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст поста')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор')
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='groups',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост')
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='posts/',
        blank=True,
        null=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Текст поста',
        related_name='comments')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments')
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Напишите комментарий')
    created = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Укажите имя подписчика',
        help_text='Подписчик',)
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='На кого подписываемся',
        help_text='Автор поста',)

    class Meta:
        ordering = ('following',)
        constraints = [models.UniqueConstraint(
            fields=['user', 'following'], name='unique_members')]
