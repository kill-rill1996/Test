from django.conf import settings
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор поста', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Пост')
    date_pub = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор комментария', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата добавления комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self',
                               verbose_name='Родительский комментарий',
                               blank=True,
                               null=True,
                               related_name='child_comment',
                               on_delete=models.CASCADE
                               )
    is_child = models.BooleanField(default=False)

    @property
    def get_parent(self):
        if not self.parent:
            return ""
        return self.parent.id

    def __str__(self):
        return f'{self.id}'